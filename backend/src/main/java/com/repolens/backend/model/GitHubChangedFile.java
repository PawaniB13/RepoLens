package com.repolens.backend.model;

import jakarta.persistence.*;

@Entity
@Table(name = "github_changed_files")
public class GitHubChangedFile {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String deliveryId;

    @Column(nullable = false)
    private String commitId;

    @Column(nullable = false)
    private String filePath;

    @Column(nullable = false)
    private String changeType;

    protected GitHubChangedFile() {
    }

    public GitHubChangedFile(
            String deliveryId,
            String commitId,
            String filePath,
            String changeType
    ) {
        this.deliveryId = deliveryId;
        this.commitId = commitId;
        this.filePath = filePath;
        this.changeType = changeType;
    }

    public Long getId() {
        return id;
    }

    public String getDeliveryId() {
        return deliveryId;
    }

    public String getCommitId() {
        return commitId;
    }

    public String getFilePath() {
        return filePath;
    }

    public String getChangeType() {
        return changeType;
    }
}