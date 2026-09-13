package com.repolens.backend.controller;

import com.repolens.backend.model.GitHubChangedFile;
import com.repolens.backend.repository.GitHubChangedFileRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/github/changed-files")
public class GitHubChangedFileController {

    private final GitHubChangedFileRepository changedFileRepository;

    public GitHubChangedFileController(
            GitHubChangedFileRepository changedFileRepository
    ) {
        this.changedFileRepository = changedFileRepository;
    }

    @GetMapping("/{deliveryId}")
    public List<GitHubChangedFile> getChangedFiles(
            @PathVariable String deliveryId
    ) {
        return changedFileRepository.findByDeliveryId(deliveryId);
    }
}