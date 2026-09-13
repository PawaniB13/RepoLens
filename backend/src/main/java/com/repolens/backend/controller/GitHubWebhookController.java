package com.repolens.backend.controller;

import com.repolens.backend.service.GitHubWebhookService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/github/webhook")
public class GitHubWebhookController {

    private final GitHubWebhookService gitHubWebhookService;

    public GitHubWebhookController(
            GitHubWebhookService gitHubWebhookService
    ) {
        this.gitHubWebhookService = gitHubWebhookService;
    }

    @PostMapping
    public ResponseEntity<String> receiveWebhook(
            @RequestHeader(
                    value = "X-GitHub-Event",
                    required = false
            ) String eventType,

            @RequestHeader(
                    value = "X-GitHub-Delivery",
                    required = false
            ) String deliveryId,

            @RequestHeader(
                    value = "X-Hub-Signature-256",
                    required = false
            ) String signature,

            @RequestBody String payload
    ) {
        gitHubWebhookService.processWebhook(
                eventType,
                deliveryId,
                signature,
                payload
        );

        return ResponseEntity.ok(
                "GitHub webhook received successfully"
        );
    }

    @GetMapping
    public ResponseEntity<String> testWebhookEndpoint() {
        return ResponseEntity.ok(
                "GitHub webhook endpoint is running. Send a POST request."
        );
    }
}