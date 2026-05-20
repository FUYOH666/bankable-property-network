package main

import (
	"bytes"
	"context"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"path/filepath"
	"strings"
	"sync"
	"syscall"
	"time"

	"github.com/skip2/go-qrcode"
	_ "github.com/mattn/go-sqlite3"
	"go.mau.fi/whatsmeow"
	waProto "go.mau.fi/whatsmeow/binary/proto"
	"go.mau.fi/whatsmeow/store/sqlstore"
	"go.mau.fi/whatsmeow/types/events"
	waLog "go.mau.fi/whatsmeow/util/log"
	"google.golang.org/protobuf/proto"
)

type bridgeState struct {
	mu            sync.RWMutex
	client        *whatsmeow.Client
	paired        bool
	lastQR        string
	lastQRAt      time.Time
	qrReady       bool
	lastPairError string
	pairCode      string
}

type consultRequest struct {
	SessionID string `json:"session_id"`
	Message   string `json:"message"`
	Channel   string `json:"channel"`
}

type consultResponse struct {
	Reply string `json:"reply"`
}

var state bridgeState

var (
	processedMu       sync.Mutex
	processedMessages = make(map[string]time.Time)
)

const (
	dedupTTL      = 10 * time.Minute
	maxMessageAge = 2 * time.Minute
)

func shouldProcessMessage(chatJID, messageID string, ts time.Time) bool {
	if messageID == "" {
		return true
	}
	if !ts.IsZero() && time.Since(ts) > maxMessageAge {
		return false
	}
	key := chatJID + ":" + messageID
	now := time.Now()
	processedMu.Lock()
	defer processedMu.Unlock()
	for k, seenAt := range processedMessages {
		if now.Sub(seenAt) > dedupTTL {
			delete(processedMessages, k)
		}
	}
	if _, seen := processedMessages[key]; seen {
		return false
	}
	processedMessages[key] = now
	return true
}

func envOr(key, fallback string) string {
	if v := strings.TrimSpace(os.Getenv(key)); v != "" {
		return v
	}
	return fallback
}

func bankableAPIURL() string {
	return strings.TrimRight(envOr("BANKABLE_API_URL", "http://localhost:8080"), "/")
}

func allowedChatJID() string {
	return strings.TrimSpace(os.Getenv("ALLOWED_CHAT_JID"))
}

func sessionPath() string {
	return envOr("WHATSAPP_SESSION_PATH", "/data/session/whatsapp.db")
}

func listenAddr() string {
	return envOr("WHATSAPP_BRIDGE_ADDR", ":8020")
}

func pairPhoneEnv() string {
	return strings.TrimSpace(os.Getenv("WHATSAPP_PAIR_PHONE"))
}

func (s *bridgeState) setQR(code string) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.lastQR = code
	s.qrReady = code != ""
	s.lastQRAt = time.Now().UTC()
}

func (s *bridgeState) getQRMeta() (code string, ready bool, ageSec int) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	age := 0
	if !s.lastQRAt.IsZero() {
		age = int(time.Since(s.lastQRAt).Seconds())
	}
	return s.lastQR, s.qrReady, age
}

func (s *bridgeState) setPairError(msg string) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.lastPairError = msg
}

func (s *bridgeState) getPairError() string {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.lastPairError
}

func (s *bridgeState) setPairCode(code string) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.pairCode = code
}

func (s *bridgeState) getPairCode() string {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.pairCode
}

func (s *bridgeState) setPaired(paired bool) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.paired = paired
}

func (s *bridgeState) isPaired() bool {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.paired
}

func callConsultAPI(ctx context.Context, chatJID, message string) (string, error) {
	payload := consultRequest{
		SessionID: "whatsapp-" + chatJID,
		Message:   message,
		Channel:   "whatsapp",
	}
	body, err := json.Marshal(payload)
	if err != nil {
		return "", err
	}

	req, err := http.NewRequestWithContext(
		ctx,
		http.MethodPost,
		bankableAPIURL()+"/api/consult/message",
		bytes.NewReader(body),
	)
	if err != nil {
		return "", err
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{Timeout: 45 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode >= 400 {
		raw, _ := io.ReadAll(resp.Body)
		return "", fmt.Errorf("consult API status %d: %s", resp.StatusCode, string(raw))
	}

	var parsed consultResponse
	if err := json.NewDecoder(resp.Body).Decode(&parsed); err != nil {
		return "", err
	}
	if strings.TrimSpace(parsed.Reply) == "" {
		return "Consultation service returned an empty reply (synthetic demo).", nil
	}
	return parsed.Reply, nil
}

func handleInboundMessage(ctx context.Context, client *whatsmeow.Client, evt *events.Message) {
	evt = evt.UnwrapRaw()
	if evt.Info.IsFromMe || evt.Message == nil {
		return
	}

	text := strings.TrimSpace(evt.Message.GetConversation())
	if text == "" && evt.Message.GetExtendedTextMessage() != nil {
		text = strings.TrimSpace(evt.Message.GetExtendedTextMessage().GetText())
	}
	if text == "" {
		return
	}

	chatJID := evt.Info.Chat.String()
	if !shouldProcessMessage(chatJID, string(evt.Info.ID), evt.Info.Timestamp) {
		slog.Info("Duplicate or stale message skipped", "id", evt.Info.ID, "chat", chatJID)
		return
	}

	if allowed := allowedChatJID(); allowed != "" && chatJID != allowed {
		slog.Info("Ignoring message from non-allowed chat", "chat", chatJID)
		return
	}

	reply, err := callConsultAPI(ctx, chatJID, text)
	if err != nil {
		slog.Error("Consult API call failed", "error", err)
		reply = "Consultation temporarily unavailable (synthetic demo). Please retry or use the web panel."
	}

	_, err = client.SendMessage(ctx, evt.Info.Chat, &waProto.Message{
		Conversation: proto.String(reply),
	})
	if err != nil {
		slog.Error("Failed to send WhatsApp reply", "error", err)
	}
}

func startWhatsApp(ctx context.Context) error {
	dbLog := waLog.Stdout("Database", "INFO", true)
	clientLog := waLog.Stdout("Client", "INFO", true)

	container, err := sqlstore.New(ctx, "sqlite3", "file:"+sessionPath()+"?_foreign_keys=on", dbLog)
	if err != nil {
		return fmt.Errorf("sqlstore: %w", err)
	}

	deviceStore, err := container.GetFirstDevice(ctx)
	if err != nil {
		return fmt.Errorf("device store: %w", err)
	}

	client := whatsmeow.NewClient(deviceStore, clientLog)
	client.AddEventHandler(func(raw interface{}) {
		switch evt := raw.(type) {
		case *events.Message:
			handleInboundMessage(ctx, client, evt)
		case *events.Connected:
			state.setPaired(true)
			state.setQR("")
			state.setPairError("")
			slog.Info("WhatsApp connected")
		case *events.PairSuccess:
			state.setPaired(true)
			state.setQR("")
			state.setPairError("")
			slog.Info("WhatsApp pair success", "jid", evt.ID.String())
		case *events.Disconnected:
			state.setPaired(false)
			slog.Warn("WhatsApp disconnected")
		case *events.LoggedOut:
			state.setPaired(false)
			state.setQR("")
			slog.Warn("WhatsApp logged out — scan QR again")
		}
	})

	state.mu.Lock()
	state.client = client
	state.mu.Unlock()

	if client.Store.ID == nil {
		qrChan, _ := client.GetQRChannel(ctx)
		if err := client.Connect(); err != nil {
			return fmt.Errorf("connect: %w", err)
		}
		go func() {
			pairCodeRequested := false
			for evt := range qrChan {
				switch evt.Event {
				case "code":
					state.setQR(evt.Code)
					slog.Info("QR code updated — open /pair (auto-refresh)", "timeout_sec", int(evt.Timeout.Seconds()))
					if phone := pairPhoneEnv(); phone != "" && !pairCodeRequested {
						pairCodeRequested = true
						time.Sleep(2 * time.Second)
						code, err := client.PairPhone(ctx, phone, true, whatsmeow.PairClientChrome, "Chrome (Mac OS)")
						if err != nil {
							slog.Error("PairPhone failed", "error", err)
							state.setPairError("pair_code_failed: " + err.Error())
						} else {
							state.setPairCode(code)
							slog.Info("Pairing code ready — GET /pair-code", "code", code)
						}
					}
				case "success":
					state.setPaired(true)
					state.setPairError("")
					slog.Info("QR channel: pairing success")
				case "timeout":
					state.setPairError("qr_timeout: scan within ~20s; open http://localhost:8020/pair for fresh QR")
					slog.Warn("QR channel timeout — refresh /pair and scan again")
				case "err-client-outdated":
					state.setPairError("client_outdated: rebuild whatsapp-bridge image (whatsmeow update)")
					slog.Error("WhatsApp rejected client as outdated")
				case "err-scanned-without-multidevice":
					state.setPairError("multidevice_required: enable Linked devices in WhatsApp settings")
					slog.Error("Phone scanned QR but multi-device / linked devices not enabled")
				case "error":
					msg := "pair_error"
					if evt.Error != nil {
						msg = evt.Error.Error()
					}
					state.setPairError(msg)
					slog.Error("QR pairing error", "error", evt.Error)
				default:
					slog.Info("QR channel event", "event", evt.Event, "error", evt.Error)
				}
			}
		}()
	} else {
		state.setPaired(true)
		if err := client.Connect(); err != nil {
			return fmt.Errorf("connect existing session: %w", err)
		}
	}

	return nil
}

func healthHandler(w http.ResponseWriter, _ *http.Request) {
	writeJSON(w, http.StatusOK, map[string]interface{}{
		"status":  "ok",
		"service": "whatsapp-bridge",
		"paired":  state.isPaired(),
	})
}

func statusHandler(w http.ResponseWriter, _ *http.Request) {
	_, ready, ageSec := state.getQRMeta()
	status := "paired"
	if !state.isPaired() {
		if ready {
			status = "waiting_for_qr_scan"
		} else {
			status = "connecting"
		}
	}
	payload := map[string]interface{}{
		"status":        status,
		"paired":        state.isPaired(),
		"qr_ready":      ready && !state.isPaired(),
		"qr_age_sec":    ageSec,
		"pair_page":     "http://localhost:8020/pair",
		"last_pair_error": state.getPairError(),
	}
	if code := state.getPairCode(); code != "" {
		payload["pair_code"] = code
		payload["pair_code_hint"] = "WhatsApp → Связанные устройства → Привязка по номеру телефона"
	}
	writeJSON(w, http.StatusOK, payload)
}

func qrHandler(w http.ResponseWriter, r *http.Request) {
	code, ready, ageSec := state.getQRMeta()
	w.Header().Set("Cache-Control", "no-store, no-cache, must-revalidate")
	w.Header().Set("Pragma", "no-cache")
	if state.isPaired() {
		writeJSON(w, http.StatusOK, map[string]string{
			"status": "paired",
			"note":   "Session already paired — no QR required.",
		})
		return
	}
	if !ready {
		http.Error(w, "QR not ready yet — retry shortly", http.StatusServiceUnavailable)
		return
	}
	if ageSec > 25 {
		http.Error(w, "QR stale — reload /pair for a fresh code", http.StatusServiceUnavailable)
		return
	}

	if r.URL.Query().Get("format") == "json" {
		png, err := qrcode.Encode(code, qrcode.Highest, 512)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		writeJSON(w, http.StatusOK, map[string]interface{}{
			"status":        "waiting_for_qr_scan",
			"qr_age_sec":    ageSec,
			"qr_png_base64": base64.StdEncoding.EncodeToString(png),
		})
		return
	}

	png, err := qrcode.Encode(code, qrcode.Highest, 512)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "image/png")
	w.WriteHeader(http.StatusOK)
	_, _ = w.Write(png)
}

func pairPageHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	w.Header().Set("Cache-Control", "no-store")
	pairCode := state.getPairCode()
	pairErr := state.getPairError()
	html := `<!DOCTYPE html>
<html lang="ru"><head>
<meta charset="utf-8"/>
<meta http-equiv="refresh" content="12"/>
<title>WhatsApp pairing</title>
<style>
body{font-family:system-ui,sans-serif;max-width:520px;margin:2rem auto;padding:0 1rem}
img{width:100%;max-width:360px;display:block;margin:1rem auto;border:1px solid #ddd}
.tip{background:#f4f4f5;padding:1rem;border-radius:8px;font-size:14px}
.err{background:#fee2e2;color:#991b1b;padding:1rem;border-radius:8px}
code{font-size:1.4rem;letter-spacing:.2em}
</style></head><body>
<h1>WhatsApp pairing</h1>
<p class="tip">QR обновляется каждые ~20 сек. <strong>Сканируй сразу после загрузки</strong> — не используй старый скриншот.</p>
<p>Телефон → WhatsApp → <strong>Связанные устройства</strong> → <strong>Привязать устройство</strong>.</p>
<img src="/qr?t=` + fmt.Sprintf("%d", time.Now().Unix()) + `" alt="WhatsApp QR"/>
`
	if pairCode != "" {
		html += `<p>Или код привязки: <code>` + pairCode + `</code><br/>
WhatsApp → Связанные устройства → <strong>Привязка по номеру телефона</strong>.</p>`
	}
	if pairErr != "" {
		html += `<p class="err">` + pairErr + `</p>`
	}
	html += `<p><a href="/status">JSON status</a> · страница авто-обновляется каждые 12 сек</p></body></html>`
	_, _ = w.Write([]byte(html))
}

func pairCodeHandler(w http.ResponseWriter, _ *http.Request) {
	code := state.getPairCode()
	if code == "" {
		writeJSON(w, http.StatusServiceUnavailable, map[string]string{
			"error": "pair_code_not_ready",
			"hint":  "Set WHATSAPP_PAIR_PHONE env (digits only, e.g. 79001234567) and restart bridge",
		})
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{
		"pair_code": code,
		"hint":      "WhatsApp → Linked devices → Link with phone number",
	})
}

func writeJSON(w http.ResponseWriter, status int, payload interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}

func main() {
	slog.SetDefault(slog.New(slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo})))

	ctx, cancel := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer cancel()

	if err := os.MkdirAll(filepath.Dir(sessionPath()), 0o755); err != nil {
		slog.Error("Failed to create session dir", "error", err)
		os.Exit(1)
	}

	if err := startWhatsApp(ctx); err != nil {
		slog.Error("WhatsApp startup failed", "error", err)
		os.Exit(1)
	}

	mux := http.NewServeMux()
	mux.HandleFunc("/healthz", healthHandler)
	mux.HandleFunc("/status", statusHandler)
	mux.HandleFunc("/qr", qrHandler)
	mux.HandleFunc("/pair", pairPageHandler)
	mux.HandleFunc("/pair-code", pairCodeHandler)
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" {
			http.NotFound(w, r)
			return
		}
		http.Redirect(w, r, "/pair", http.StatusFound)
	})

	server := &http.Server{
		Addr:              listenAddr(),
		Handler:           mux,
		ReadHeaderTimeout: 5 * time.Second,
	}

	go func() {
		slog.Info("WhatsApp bridge listening", "addr", listenAddr(), "bankable_api", bankableAPIURL())
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			slog.Error("HTTP server failed", "error", err)
			cancel()
		}
	}()

	<-ctx.Done()
	shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer shutdownCancel()
	_ = server.Shutdown(shutdownCtx)

	state.mu.RLock()
	client := state.client
	state.mu.RUnlock()
	if client != nil {
		client.Disconnect()
	}
}
