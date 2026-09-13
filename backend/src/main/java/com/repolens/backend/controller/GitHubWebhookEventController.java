package com.repolens.backend.controller;

import com.repolens.backend.model.GitHubWebhookEvent;
import com.repolens.backend.repository.GitHubWebhookEventRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/github/webhook/events")
public class GitHubWebhookEventController {

    private final GitHubWebhookEventRepository webhookEventRepository;

    public GitHubWebhookEventController(
            GitHubWebhookEventRepository webhookEventRepository
    ) {
        this.webhookEventRepository = webhookEventRepository;
    }

    @GetMapping
    public List<GitHubWebhookEvent> getWebhookEvents() {
        return webhookEventRepository.findAll();
    }
}