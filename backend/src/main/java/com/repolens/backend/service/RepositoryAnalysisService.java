package com.repolens.backend.service;

import com.repolens.backend.model.Repository;
import com.repolens.backend.model.RepositoryAnalysis;
import com.repolens.backend.model.RepositoryFile;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RepositoryAnalysisService {

    private final RepositoryService repositoryService;
    private final RepositoryFileService repositoryFileService;

    public RepositoryAnalysisService(
            RepositoryService repositoryService,
            RepositoryFileService repositoryFileService
    ) {
        this.repositoryService = repositoryService;
        this.repositoryFileService = repositoryFileService;
    }

    public RepositoryAnalysis analyzeRepository(Long repositoryId) {

        Repository repository =
                repositoryService.getRepository(repositoryId);

        List<RepositoryFile> files =
                repositoryFileService.getFiles(repositoryId);

        int totalFiles = files.size();

        int javaFiles = (int) files.stream()
                .filter(file ->
                        file.getFileName() != null
                                && file.getFileName()
                                .toLowerCase()
                                .endsWith(".java")
                )
                .count();

        int javascriptFiles = (int) files.stream()
                .filter(file ->
                        file.getFileName() != null
                                && (
                                file.getFileName()
                                        .toLowerCase()
                                        .endsWith(".js")
                                        || file.getFileName()
                                        .toLowerCase()
                                        .endsWith(".jsx")
                        )
                )
                .count();

        RepositoryAnalysis analysis =
                new RepositoryAnalysis(
                        repositoryId,
                        repository.getName(),
                        totalFiles,
                        javaFiles,
                        javascriptFiles
                );

        analysis.setDefaultBranch("main");

        return analysis;
    }
}