package com.repolens.backend.repository;

import com.repolens.backend.model.RepositoryFile;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface RepositoryFileRepository
        extends JpaRepository<RepositoryFile, Long> {

    List<RepositoryFile> findByRepositoryId(Long repositoryId);
}