package com.repolens.backend.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class GitHubWebhookService {

    private static final Set<String> PROCESSED_DELIVERIES =
            ConcurrentHashMap.newKeySet();

    private final ObjectMapper objectMapper;

    public GitHubWebhookService(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    public void processWebhook(
            String eventType,
            String deliveryId,
            String signature,
            String payload
    ) {
        if (eventType == null || eventType.isBlank()) {
            throw new IllegalArgumentException(
                    "Missing X-GitHub-Event header"
            );
        }

        if (deliveryId != null && !deliveryId.isBlank()) {
            boolean firstDelivery =
                    PROCESSED_DELIVERIES.add(deliveryId);

            if (!firstDelivery) {
                System.out.println(
                        "Ignoring duplicate GitHub delivery: "
                                + deliveryId
                );
                return;
            }
        }

        try {
            JsonNode root = objectMapper.readTree(payload);

            JsonNode repositoryNode = root.path("repository");
            JsonNode refNode = root.path("ref");

            String repositoryFullName =
                    repositoryNode.path("full_name").asText(null);

            String branch = extractBranch(eventType, root, refNode);

            System.out.println("GitHub event: " + eventType);
            System.out.println("Repository: " + repositoryFullName);
            System.out.println("Branch: " + branch);

            switch (eventType) {
                case "push" -> handlePushEvent(
                        repositoryFullName,
                        branch,
                        root
                );

                case "pull_request" -> handlePullRequestEvent(
                        repositoryFullName,
                        root
                );

                case "ping" -> System.out.println(
                        "GitHub webhook ping received"
                );

                default -> System.out.println(
                        "Ignoring unsupported GitHub event: "
                                + eventType
                );
            }

        } catch (Exception exception) {
            throw new IllegalArgumentException(
                    "Invalid GitHub webhook payload",
                    exception
            );
        }
    }

    private String extractBranch(
            String eventType,
            JsonNode root,
            JsonNode refNode
    ) {
        if ("push".equals(eventType)) {
            String ref = refNode.asText("");

            if (ref.startsWith("refs/heads/")) {
                return ref.substring("refs/heads/".length());
            }

            return ref;
        }

        if ("pull_request".equals(eventType)) {
            return root.path("pull_request")
                    .path("base")
                    .path("ref")
                    .asText(null);
        }

        return null;
    }

    private void handlePushEvent(
            String repositoryFullName,
            String branch,
            JsonNode root
    ) {
        int changedFileCount =
                root.path("commits").size();

        System.out.println(
                "Push event received for "
                        + repositoryFullName
                        + " on branch "
                        + branch
                        + ". Commits: "
                        + changedFileCount
        );

        // Next step:
        // 1. Fetch changed files from GitHub.
        // 2. Store the webhook event.
        // 3. Trigger repository analysis.
    }

    private void handlePullRequestEvent(
            String repositoryFullName,
            JsonNode root
    ) {
        String action =
                root.path("action").asText(null);

        System.out.println(
                "Pull request event received for "
                        + repositoryFullName
                        + ". Action: "
                        + action
        );

        // Next step:
        // 1. Check opened/synchronize/reopened actions.
        // 2. Fetch changed files.
        // 3. Trigger analysis if required.
    }
}