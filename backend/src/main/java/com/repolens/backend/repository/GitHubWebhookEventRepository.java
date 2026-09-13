package com.repolens.backend.repository;

import com.repolens.backend.model.GitHubWebhookEvent;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface GitHubWebhookEventRepository
        extends JpaRepository<GitHubWebhookEvent, Long> {

    boolean existsByDeliveryId(String deliveryId);

    List<GitHubWebhookEvent> findByEventType(String eventType);
}