package com.repolens.backend.service;

import com.repolens.backend.model.RepositoryAnalysis;
import com.repolens.backend.model.RepositoryFile;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RepositoryAnalysisService {

    private final RepositoryFileService repositoryFileService;

    public RepositoryAnalysisService(RepositoryFileService repositoryFileService) {
        this.repositoryFileService = repositoryFileService;
    }

    public RepositoryAnalysis analyzeRepository(Long repositoryId) {

        if (repositoryId == null || repositoryId <= 0) {
            throw new IllegalArgumentException("Repository ID must be positive");
        }

        List<RepositoryFile> files =
                repositoryFileService.getFiles(repositoryId);

        int totalFiles = files.size();

        int javaFiles = (int) files.stream()
                .filter(file -> "Java".equalsIgnoreCase(file.getFileType()))
                .count();

        int javascriptFiles = (int) files.stream()
                .filter(file -> "JavaScript".equalsIgnoreCase(file.getFileType()))
                .count();

        return new RepositoryAnalysis(
                repositoryId,
                "RepoLens",
                totalFiles,
                javaFiles,
                javascriptFiles
        );
    }
}