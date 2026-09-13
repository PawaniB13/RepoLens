package com.repolens.backend.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.repolens.backend.model.GitHubChangedFile;
import com.repolens.backend.model.GitHubWebhookEvent;
import com.repolens.backend.repository.GitHubChangedFileRepository;
import com.repolens.backend.repository.GitHubWebhookEventRepository;
import org.springframework.stereotype.Service;

@Service
public class GitHubWebhookService {

    private final ObjectMapper objectMapper;
    private final GitHubWebhookEventRepository webhookEventRepository;
    private final GitHubChangedFileRepository changedFileRepository;

    public GitHubWebhookService(
            ObjectMapper objectMapper,
            GitHubWebhookEventRepository webhookEventRepository,
            GitHubChangedFileRepository changedFileRepository
    ) {
        this.objectMapper = objectMapper;
        this.webhookEventRepository = webhookEventRepository;
        this.changedFileRepository = changedFileRepository;
    }

    public void processWebhook(
            String eventType,
            String deliveryId,
            String signature,
            String payload
    ) {
        if (eventType == null || eventType.isBlank()) {
            throw new IllegalArgumentException(
                    "Missing GitHub event type"
            );
        }

        if (deliveryId == null || deliveryId.isBlank()) {
            throw new IllegalArgumentException(
                    "Missing GitHub delivery ID"
            );
        }

        if (payload == null || payload.isBlank()) {
            throw new IllegalArgumentException(
                    "Missing GitHub webhook payload"
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

            GitHubWebhookEvent webhookEvent =
                    new GitHubWebhookEvent(
                            deliveryId,
                            eventType,
                            repository,
                            branch,
                            sender
                    );

            webhookEventRepository.save(webhookEvent);

            if ("push".equals(eventType)) {
                saveChangedFiles(root, deliveryId);
            }

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

    private void saveChangedFiles(
            JsonNode root,
            String deliveryId
    ) {
        JsonNode commits = root.path("commits");

        if (!commits.isArray()) {
            System.out.println(
                    "No commits found in push webhook payload"
            );
            return;
        }

        for (JsonNode commit : commits) {
            String commitId = commit.path("id")
                    .asText("unknown");

            saveFileList(
                    deliveryId,
                    commitId,
                    commit.path("added"),
                    "ADDED"
            );

            saveFileList(
                    deliveryId,
                    commitId,
                    commit.path("modified"),
                    "MODIFIED"
            );

            saveFileList(
                    deliveryId,
                    commitId,
                    commit.path("removed"),
                    "REMOVED"
            );
        }
    }

    private void saveFileList(
            String deliveryId,
            String commitId,
            JsonNode files,
            String changeType
    ) {
        if (!files.isArray()) {
            return;
        }

        for (JsonNode file : files) {
            String filePath = file.asText();

            GitHubChangedFile changedFile =
                    new GitHubChangedFile(
                            deliveryId,
                            commitId,
                            filePath,
                            changeType
                    );

            changedFileRepository.save(changedFile);

            System.out.println(
                    changeType + " file saved: " + filePath
            );
        }
    }
}