package com.repolens.backend.service;

import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class GitHubWebhookService {

    public WebhookData parsePushPayload(Map<String, Object> payload) {
        if (payload == null) {
            throw new IllegalArgumentException("Webhook payload cannot be null");
        }

        Map<String, Object> repository =
                castMap(payload.get("repository"));

        Map<String, Object> owner =
                castMap(repository.get("owner"));

        String ownerLogin = getString(owner, "login");
        String repositoryName = getString(repository, "name");
        String repositoryUrl = getString(repository, "html_url");

        String afterCommit = getString(payload, "after");

        List<String> changedFiles = extractChangedFiles(payload);

        return new WebhookData(
                ownerLogin,
                repositoryName,
                repositoryUrl,
                afterCommit,
                changedFiles
        );
    }

    private List<String> extractChangedFiles(Map<String, Object> payload) {
        Object commitsValue = payload.get("commits");

        if (!(commitsValue instanceof List<?> commits)) {
            return List.of();
        }

        return commits.stream()
                .filter(Map.class::isInstance)
                .map(commit -> castMap(commit))
                .flatMap(commit -> {
                    List<String> files = new java.util.ArrayList<>();

                    addFiles(commit.get("added"), files);
                    addFiles(commit.get("modified"), files);
                    addFiles(commit.get("removed"), files);

                    return files.stream();
                })
                .distinct()
                .toList();
    }

    private void addFiles(Object value, List<String> files) {
        if (value instanceof List<?> values) {
            values.stream()
                    .filter(String.class::isInstance)
                    .map(String.class::cast)
                    .forEach(files::add);
        }
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> castMap(Object value) {
        if (!(value instanceof Map<?, ?>)) {
            return Map.of();
        }

        return (Map<String, Object>) value;
    }

    private String getString(Map<String, Object> map, String key) {
        Object value = map.get(key);
        return value == null ? null : value.toString();
    }

    public record WebhookData(
            String owner,
            String repository,
            String repositoryUrl,
            String commitSha,
            List<String> changedFiles
    ) {
    }
}