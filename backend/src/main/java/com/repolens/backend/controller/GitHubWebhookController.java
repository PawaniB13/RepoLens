package com.repolens.backend.controller;

import com.repolens.backend.service.GitHubWebhookService;
import com.repolens.backend.service.RepositoryService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/webhooks/github")
public class GitHubWebhookController {

    private final GitHubWebhookService gitHubWebhookService;
    private final RepositoryService repositoryService;

    public GitHubWebhookController(
            GitHubWebhookService gitHubWebhookService,
            RepositoryService repositoryService
    ) {
        this.gitHubWebhookService = gitHubWebhookService;
        this.repositoryService = repositoryService;
    }

    @PostMapping
    public ResponseEntity<Map<String, Object>> receiveWebhook(
            @RequestHeader(value = "X-GitHub-Event", required = false)
            String event,

            @RequestBody(required = false)
            Map<String, Object> payload
    ) {
        if (!"push".equalsIgnoreCase(event)) {
            return ResponseEntity.ok(
                    Map.of(
                            "status", "ignored",
                            "event", event == null ? "unknown" : event
                    )
            );
        }

        GitHubWebhookService.WebhookData webhookData =
                gitHubWebhookService.parsePushPayload(payload);

        return ResponseEntity.ok(
                Map.of(
                        "status", "received",
                        "event", "push",
                        "owner", webhookData.owner(),
                        "repository", webhookData.repository(),
                        "commitSha", webhookData.commitSha(),
                        "changedFiles", webhookData.changedFiles()
                )
        );
    }
}