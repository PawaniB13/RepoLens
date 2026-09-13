package com.repolens.backend.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(
        name = "github_webhook_events",
        uniqueConstraints = @UniqueConstraint(columnNames = "deliveryId")
)
public class GitHubWebhookEvent {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String deliveryId;

    @Column(nullable = false)
    private String eventType;

    private String repository;

    private String branch;

    private String sender;

    @Column(nullable = false)
    private LocalDateTime receivedAt;

    protected GitHubWebhookEvent() {
    }

    public GitHubWebhookEvent(
            String deliveryId,
            String eventType,
            String repository,
            String branch,
            String sender
    ) {
        this.deliveryId = deliveryId;
        this.eventType = eventType;
        this.repository = repository;
        this.branch = branch;
        this.sender = sender;
        this.receivedAt = LocalDateTime.now();
    }

    public Long getId() {
        return id;
    }

    public String getDeliveryId() {
        return deliveryId;
    }

    public String getEventType() {
        return eventType;
    }

    public String getRepository() {
        return repository;
    }

    public String getBranch() {
        return branch;
    }

    public String getSender() {
        return sender;
    }

    public LocalDateTime getReceivedAt() {
        return receivedAt;
    }
}