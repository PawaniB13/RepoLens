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

            @RequestBody String payload
    ) {
        gitHubWebhookService.processWebhook(eventType, payload);

        return ResponseEntity.ok(
                "GitHub webhook received successfully"
        );
    }

    @GetMapping
    public ResponseEntity<String> testWebhookEndpoint() {
        return ResponseEntity.ok(
                "GitHub webhook endpoint is running. Send a POST request to use it."
        );
    }
}