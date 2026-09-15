package com.repolens.backend.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/webhooks/github")
public class GitHubWebhookController {

    @PostMapping
    public ResponseEntity<Map<String, String>> receiveWebhook(
            @RequestHeader(value = "X-GitHub-Event", required = false)
            String event,

            @RequestBody(required = false)
            Map<String, Object> payload
    ) {
        if ("push".equalsIgnoreCase(event)) {
            return ResponseEntity.ok(
                    Map.of(
                            "status", "received",
                            "event", "push"
                    )
            );
        }

        return ResponseEntity.ok(
                Map.of(
                        "status", "ignored",
                        "event", event == null ? "unknown" : event
                )
        );
    }
}