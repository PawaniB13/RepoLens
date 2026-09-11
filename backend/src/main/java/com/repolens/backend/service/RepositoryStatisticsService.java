package com.repolens.backend.service;

import com.repolens.backend.model.RepositoryFile;
import com.repolens.backend.model.RepositoryStatistics;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RepositoryStatisticsService {

    private final RepositoryFileService repositoryFileService;

    public RepositoryStatisticsService(RepositoryFileService repositoryFileService) {
        this.repositoryFileService = repositoryFileService;
    }

    public RepositoryStatistics getStatistics(Long repositoryId) {

        if (repositoryId == null || repositoryId <= 0) {
            throw new IllegalArgumentException("Repository ID must be positive");
        }

        List<RepositoryFile> files = repositoryFileService.getFiles(repositoryId);

        int totalFiles = files.size();

        int javaFiles = (int) files.stream()
                .filter(file -> "Java".equalsIgnoreCase(file.getFileType()))
                .count();

        int javascriptFiles = (int) files.stream()
                .filter(file -> "JavaScript".equalsIgnoreCase(file.getFileType()))
                .count();

        int otherFiles = totalFiles - javaFiles - javascriptFiles;

        return new RepositoryStatistics(
                repositoryId,
                "RepoLens",
                totalFiles,
                javaFiles,
                javascriptFiles,
                otherFiles
        );
    }
}