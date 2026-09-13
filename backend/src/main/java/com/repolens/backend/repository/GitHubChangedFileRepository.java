package com.repolens.backend.repository;

import com.repolens.backend.model.GitHubChangedFile;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface GitHubChangedFileRepository
        extends JpaRepository<GitHubChangedFile, Long> {

    List<GitHubChangedFile> findByDeliveryId(String deliveryId);
}