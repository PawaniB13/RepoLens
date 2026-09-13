package com.repolens.backend.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.repolens.backend.model.GitHubWebhookEvent;
import com.repolens.backend.repository.GitHubWebhookEventRepository;
import org.springframework.stereotype.Service;

@Service
public class GitHubWebhookService {

    private final ObjectMapper objectMapper;
    private final GitHubWebhookEventRepository webhookEventRepository;

    public GitHubWebhookService(
            ObjectMapper objectMapper,
            GitHubWebhookEventRepository webhookEventRepository
    ) {
        this.objectMapper = objectMapper;
        this.webhookEventRepository = webhookEventRepository;
    }

    public void processWebhook(
            String eventType,
            String deliveryId,
            String signature,
            String payload
    ) {
        if (deliveryId == null || deliveryId.isBlank()) {
            throw new IllegalArgumentException(
                    "Missing GitHub delivery ID"
            );
        }

        if (webhookEventRepository.existsByDeliveryId(deliveryId)) {
            System.out.println(
                    "Duplicate GitHub webhook ignored: " + deliveryId
            );
            return;
        }

        try {
            JsonNode root = objectMapper.readTree(payload);

            String repository = root.path("repository")
                    .path("full_name")
                    .asText(null);

            String branch = root.path("ref")
                    .asText(null);

            String sender = root.path("sender")
                    .path("login")
                    .asText(null);
                    if ("push".equals(eventType)) {
    printChangedFiles(root);
}

            GitHubWebhookEvent webhookEvent =
                    new GitHubWebhookEvent(
                            deliveryId,
                            eventType,
                            repository,
                            branch,
                            sender
                    );

            webhookEventRepository.save(webhookEvent);

            System.out.println("GitHub webhook saved");
            System.out.println("Event type: " + eventType);
            System.out.println("Delivery ID: " + deliveryId);
            System.out.println("Repository: " + repository);
            System.out.println("Branch: " + branch);
            System.out.println("Sender: " + sender);

        } catch (Exception exception) {
            throw new IllegalArgumentException(
                    "Invalid GitHub webhook payload",
                    exception
            );
        }
    }
    private void printChangedFiles(JsonNode root) {
    JsonNode commits = root.path("commits");

    if (!commits.isArray()) {
        System.out.println("No commits found in webhook payload");
        return;
    }

    for (JsonNode commit : commits) {
        String commitId = commit.path("id").asText("unknown");

        System.out.println("Commit: " + commitId);

        printFileList("Added", commit.path("added"));
        printFileList("Modified", commit.path("modified"));
        printFileList("Removed", commit.path("removed"));
    }
}

private void printFileList(String action, JsonNode files) {
    if (!files.isArray()) {
        return;
    }

    for (JsonNode file : files) {
        System.out.println(action + " file: " + file.asText());
    }
}
}