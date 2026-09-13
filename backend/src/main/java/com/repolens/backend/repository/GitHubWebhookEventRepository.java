package com.repolens.backend.repository;

import com.repolens.backend.model.GitHubWebhookEvent;
import org.springframework.data.jpa.repository.JpaRepository;

public interface GitHubWebhookEventRepository
        extends JpaRepository<GitHubWebhookEvent, Long> {

    boolean existsByDeliveryId(String deliveryId);
}