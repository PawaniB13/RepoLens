package com.repolens.backend.service;

import com.repolens.backend.model.Repository;
import com.repolens.backend.model.RepositoryFile;
import com.repolens.backend.model.RepositoryStatistics;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RepositoryStatisticsService {

    private final RepositoryFileService repositoryFileService;
    private final RepositoryService repositoryService;

    @Autowired
    public RepositoryStatisticsService(
            RepositoryFileService repositoryFileService,
            RepositoryService repositoryService) {

        this.repositoryFileService = repositoryFileService;
        this.repositoryService = repositoryService;
    }

    // Constructor used by existing unit tests
    public RepositoryStatisticsService(
            RepositoryFileService repositoryFileService) {

        this.repositoryFileService = repositoryFileService;
        this.repositoryService = null;
    }

    public RepositoryStatistics getStatistics(Long repositoryId) {

        if (repositoryId == null || repositoryId <= 0) {
            throw new IllegalArgumentException("Repository ID must be positive");
        }

        List<RepositoryFile> files =
                repositoryFileService.getFiles(repositoryId);

        int totalFiles = files.size();

        int javaFiles = (int) files.stream()
                .filter(file ->
                        "Java".equalsIgnoreCase(file.getFileType()))
                .count();

        int javascriptFiles = (int) files.stream()
                .filter(file ->
                        "JavaScript".equalsIgnoreCase(file.getFileType()))
                .count();

        int otherFiles = totalFiles - javaFiles - javascriptFiles;

        String repositoryName = "RepoLens";

        if (repositoryService != null) {
            Repository repository =
                    repositoryService.getRepository(repositoryId);

            repositoryName = repository.getName();
        }

        return new RepositoryStatistics(
                repositoryId,
                repositoryName,
                totalFiles,
                javaFiles,
                javascriptFiles,
                otherFiles
        );
    }
}