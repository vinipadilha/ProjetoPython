/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
 /*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
 /*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 /*!50503 SET NAMES utf8mb4 */;
 /*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
 /*!40103 SET TIME_ZONE='+00:00' */;
 /*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
 /*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
 /*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
 /*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS `plataformatreinamentos`
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE `plataformatreinamentos`;

DROP TABLE IF EXISTS `matricula`;
DROP TABLE IF EXISTS `recurso`;
DROP TABLE IF EXISTS `turma`;
DROP TABLE IF EXISTS `treinamento`;
DROP TABLE IF EXISTS `usuario`;
DROP TABLE IF EXISTS `perfil`;

-- perfil (sem UNIQUE no nome)
CREATE TABLE `perfil` (
  `pefId` INT NOT NULL AUTO_INCREMENT,
  `pefNome` VARCHAR(100) NOT NULL,
  `pefCadastradoEm` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`pefId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `perfil` (`pefId`,`pefNome`,`pefCadastradoEm`) VALUES
  (1,'ADMIN','2025-11-02 20:58:38'),
  (2,'ESTUDANTE','2025-11-02 20:58:38')
ON DUPLICATE KEY UPDATE `pefNome`=VALUES(`pefNome`);

-- usuario (sem UNIQUE no email)
CREATE TABLE `usuario` (
  `usuId` INT NOT NULL AUTO_INCREMENT,
  `usuPefId` INT NOT NULL,
  `usuNome` VARCHAR(200) NOT NULL,
  `usuEmail` VARCHAR(200) NOT NULL,
  `usuSenha` TEXT,
  `usuTelefone` VARCHAR(32) DEFAULT NULL,
  `usuCadastradoEm` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_login` DATETIME(6) DEFAULT NULL,
  `is_active` TINYINT(1) NOT NULL DEFAULT 1,
  `is_staff` TINYINT(1) NOT NULL DEFAULT 0,
  `is_superuser` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`usuId`),
  KEY `idx_usuario_email` (`usuEmail`),
  KEY `fk_usuario_perfil1_idx` (`usuPefId`),
  CONSTRAINT `fk_usuario_perfil` FOREIGN KEY (`usuPefId`)
    REFERENCES `perfil` (`pefId`) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `usuario`
  (`usuId`,`usuPefId`,`usuNome`,`usuEmail`,`usuSenha`,`usuTelefone`,
   `usuCadastradoEm`,`last_login`,`is_active`,`is_staff`,`is_superuser`)
VALUES
  (1,1,'Administrador','admin@email.com',
   'pbkdf2_sha256$1000000$t53SiXs0NZpnONqJVfWWWg$4gM1vk0QVueI/+nI7uMw3AiDdOHBVVUafrS113jvA54=',
   '41991226168','2025-11-02 21:43:44','2025-11-03 04:07:13.597910',1,0,0),
  (2,2,'Estudante','estudante@email.com',
   'pbkdf2_sha256$1000000$BYSTRcdFQfGY16KBITZpXf$KD2s7yIEby5tql9lhmR5VeKhBCI9ErqcRcykGVWGT7o=',
   '4199999999','2025-11-03 04:08:15','2025-11-03 04:21:06.818307',1,0,0)
ON DUPLICATE KEY UPDATE `usuEmail`=VALUES(`usuEmail`);

-- treinamento
CREATE TABLE `treinamento` (
  `treId` INT NOT NULL AUTO_INCREMENT,
  `treNome` VARCHAR(200) NOT NULL,
  `treDescricao` TEXT,
  `treCadastradoEm` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`treId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `treinamento`
  (`treId`,`treNome`,`treDescricao`,`treCadastradoEm`)
VALUES
  (1,'Teste de Treinamento','Teste descrição treinamento','2025-11-03 01:26:31')
ON DUPLICATE KEY UPDATE `treNome`=VALUES(`treNome`);

-- turma
CREATE TABLE `turma` (
  `truId` INT NOT NULL AUTO_INCREMENT,
  `truTreId` INT NOT NULL,
  `truNome` VARCHAR(200) NOT NULL,
  `truDataInicio` DATE DEFAULT NULL,
  `truDataConclusao` DATE DEFAULT NULL,
  `truLinkAcesso` VARCHAR(200) DEFAULT NULL,
  `truCadastradoEm` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`truId`),
  KEY `fk_turma_treinamento_idx` (`truTreId`),
  CONSTRAINT `fk_turma_treinamento` FOREIGN KEY (`truTreId`)
    REFERENCES `treinamento` (`treId`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `turma`
  (`truId`,`truTreId`,`truNome`,`truDataInicio`,`truDataConclusao`,
   `truLinkAcesso`,`truCadastradoEm`)
VALUES
  (1,1,'Turma Futura','2025-11-13','2025-12-02','https://linkacesso.com/','2025-11-03 01:33:24'),
  (2,1,'Turma Atual','2025-11-02','2026-01-02','https://linkacesso.com/','2025-11-03 05:37:45')
ON DUPLICATE KEY UPDATE `truNome`=VALUES(`truNome`);

-- recurso
CREATE TABLE `recurso` (
  `recId` INT NOT NULL AUTO_INCREMENT,
  `recTruId` INT NOT NULL,
  `recTipo` ENUM('VIDEO','PDF','ZIP') NOT NULL,
  `recAcessoPrevio` TINYINT(1) NOT NULL DEFAULT 0,
  `recDraft` TINYINT(1) NOT NULL DEFAULT 0,
  `recNome` VARCHAR(200) NOT NULL,
  `recDescricao` TEXT,
  `recArquivoPath` VARCHAR(500) DEFAULT NULL,
  `recCadastradoEm` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`recId`),
  KEY `fk_recurso_turma1_idx` (`recTruId`),
  CONSTRAINT `fk_recurso_turma` FOREIGN KEY (`recTruId`)
    REFERENCES `turma` (`truId`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `recurso`
  (`recId`,`recTruId`,`recTipo`,`recAcessoPrevio`,`recDraft`,
   `recNome`,`recDescricao`,`recArquivoPath`,`recCadastradoEm`)
VALUES
  (1,1,'PDF',0,0,'Recurso PDF - Não prévio e não rascunho','teste descrção recurso',
   '/media/recursos/turma_1/recurso-pdf-nao-previo-e-nao-rascunho_20251103_031853.pdf','2025-11-03 03:49:44'),
  (2,1,'PDF',1,0,'Recurso PDF - Acesso prévio','descricao',
   '/media/recursos/turma_1/recurso-pdf-acesso-previo_20251103_031833.pdf','2025-11-03 03:55:50'),
  (4,1,'PDF',1,1,'Recurso PDF - Acesso prévio e rascunho','descricao',
   '/media/recursos/turma_1/recurso-pdf-acesso-previo-e-rascunho_20251103_031841.pdf','2025-11-03 03:56:40'),
  (8,1,'VIDEO',1,0,'Recurso Vídeo - Acesso prévio','Descrição',
   '/media/videos/turma_1/recurso-video-acesso-previo_20251103_031900.mp4','2025-11-03 06:07:20'),
  (9,2,'PDF',0,0,'Recurso PDF','Descrição',
   '/media/recursos/turma_2/recurso-pdf_20251103_031918.pdf','2025-11-03 06:15:13'),
  (10,2,'VIDEO',0,0,'Recurso Vídeo','Descrição',
   '/media/videos/turma_2/recurso-video_20251103_031942.mp4','2025-11-03 06:19:42')
ON DUPLICATE KEY UPDATE `recNome`=VALUES(`recNome`);

-- matricula (sem UNIQUE; mantidos índices não exclusivos)
CREATE TABLE `matricula` (
  `matId` INT NOT NULL AUTO_INCREMENT,
  `matTruId` INT NOT NULL,
  `matUsuId` INT NOT NULL,
  `matCadastradoEm` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`matId`),
  KEY `fk_matricula_turma1_idx` (`matTruId`),
  KEY `fk_matricula_usuario1_idx` (`matUsuId`),
  CONSTRAINT `fk_matricula_turma` FOREIGN KEY (`matTruId`)
    REFERENCES `turma` (`truId`)
    ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT `fk_matricula_usuario` FOREIGN KEY (`matUsuId`)
    REFERENCES `usuario` (`usuId`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `matricula`
  (`matId`,`matTruId`,`matUsuId`,`matCadastradoEm`)
VALUES
  (2,1,2,'2025-11-03 04:50:18'),
  (4,2,2,'2025-11-03 05:40:41')
ON DUPLICATE KEY UPDATE `matCadastradoEm`=VALUES(`matCadastradoEm`);

 /*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
 /*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
 /*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
 /*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
 /*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
 /*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
 /*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
 /*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
