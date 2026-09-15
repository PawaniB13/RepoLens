package com.repolens.backend.controller;

import com.repolens.backend.service.GitHubWebhookService;
import com.repolens.backend.service.RepositoryFileService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/webhooks/github")
public class GitHubWebhookController {

    private final GitHubWebhookService gitHubWebhookService;
    private final RepositoryFileService repositoryFileService;

    public GitHubWebhookController(
            GitHubWebhookService gitHubWebhookService,
            RepositoryFileService repositoryFileService
    ) {
        this.gitHubWebhookService = gitHubWebhookService;
        this.repositoryFileService = repositoryFileService;
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

        Map<String, Object> response = new HashMap<>();

        response.put("status", "received");
        response.put("event", "push");
        response.put("owner", webhookData.owner());
        response.put("repository", webhookData.repository());
        response.put("commitSha", webhookData.commitSha());
        response.put("changedFiles", webhookData.changedFiles());

        try {
            repositoryFileService.refreshFilesByRepositoryUrl(
                    webhookData.repositoryUrl()
            );

            response.put("refreshStatus", "completed");
        } catch (Exception exception) {
            response.put("refreshStatus", "failed");
            response.put("refreshMessage", exception.getMessage());
        }

        return ResponseEntity.ok(response);
    }
}