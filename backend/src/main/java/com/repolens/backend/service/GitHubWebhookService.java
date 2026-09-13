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
}