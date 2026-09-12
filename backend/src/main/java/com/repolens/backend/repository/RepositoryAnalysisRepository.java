package com.repolens.backend.repository;

import com.repolens.backend.model.RepositoryAnalysis;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface RepositoryAnalysisRepository
        extends JpaRepository<RepositoryAnalysis, Long> {

    Optional<RepositoryAnalysis> findByRepositoryId(Long repositoryId);
}
