-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: cesizen_db
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `api_exercicerespiration`
--

DROP TABLE IF EXISTS `api_exercicerespiration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_exercicerespiration` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `duree_inspiration` int(11) NOT NULL,
  `duree_apnee` int(11) NOT NULL,
  `duree_expiration` int(11) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_exercicerespiration`
--

LOCK TABLES `api_exercicerespiration` WRITE;
/*!40000 ALTER TABLE `api_exercicerespiration` DISABLE KEYS */;
INSERT INTO `api_exercicerespiration` VALUES (1,'748',7,4,8,'Moyen'),(2,'55',5,0,5,'facile'),(3,'46',4,0,6,'facile');
/*!40000 ALTER TABLE `api_exercicerespiration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_historiqueexercice`
--

DROP TABLE IF EXISTS `api_historiqueexercice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_historiqueexercice` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `date_effectue` datetime(6) NOT NULL,
  `duree_totale` int(11) NOT NULL,
  `commentaire` longtext DEFAULT NULL,
  `exercice_id` bigint(20) NOT NULL,
  `utilisateur_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_historiqueexerci_exercice_id_78bcd56a_fk_api_exerc` (`exercice_id`),
  KEY `api_historiqueexerci_utilisateur_id_053c92c1_fk_api_utili` (`utilisateur_id`),
  CONSTRAINT `api_historiqueexerci_exercice_id_78bcd56a_fk_api_exerc` FOREIGN KEY (`exercice_id`) REFERENCES `api_exercicerespiration` (`id`),
  CONSTRAINT `api_historiqueexerci_utilisateur_id_053c92c1_fk_api_utili` FOREIGN KEY (`utilisateur_id`) REFERENCES `api_utilisateur` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_historiqueexercice`
--

LOCK TABLES `api_historiqueexercice` WRITE;
/*!40000 ALTER TABLE `api_historiqueexercice` DISABLE KEYS */;
INSERT INTO `api_historiqueexercice` VALUES (1,'2025-06-18 16:32:35.408609',60,'Test manuel',1,2),(2,'2025-06-18 16:43:39.850883',19,'Effectué depuis la séance',1,2),(3,'2025-06-18 16:46:53.961858',19,'super !\n',1,2),(4,'2025-06-18 17:03:31.405176',19,NULL,1,2),(5,'2025-06-18 17:06:12.554652',1,NULL,1,2),(6,'2025-06-18 19:26:29.347439',3,NULL,1,2),(7,'2025-06-18 20:54:18.365702',2,NULL,1,2),(8,'2025-06-19 16:27:05.565292',2,NULL,1,2),(9,'2025-06-21 10:20:38.342383',2,NULL,1,2),(10,'2025-06-21 10:26:07.012903',19,NULL,1,2),(11,'2025-06-22 12:16:07.979828',3,NULL,1,1),(12,'2025-06-22 12:20:17.166330',5,NULL,2,1),(13,'2025-06-22 12:50:41.583998',3,NULL,2,6),(14,'2025-06-24 19:23:01.021477',1,NULL,2,2),(15,'2025-06-24 19:23:15.086578',2,NULL,2,2),(16,'2025-06-24 19:23:26.342756',10,NULL,2,2),(17,'2025-06-24 19:24:27.302460',3,NULL,1,2),(18,'2025-06-25 16:17:06.153027',1,NULL,1,10),(19,'2025-06-30 08:21:27.852430',1,NULL,1,2),(20,'2025-06-30 13:41:24.035914',2,NULL,1,11),(21,'2025-07-01 08:55:24.891905',1,NULL,1,11),(22,'2025-07-03 07:33:32.391351',15,NULL,1,1);
/*!40000 ALTER TABLE `api_historiqueexercice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_information`
--

DROP TABLE IF EXISTS `api_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_information` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `titre` varchar(200) NOT NULL,
  `contenu` longtext NOT NULL,
  `date_creation` datetime(6) NOT NULL,
  `date_modification` datetime(6) NOT NULL,
  `createur_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_information_createur_id_7a1345c0_fk_api_utilisateur_id` (`createur_id`),
  CONSTRAINT `api_information_createur_id_7a1345c0_fk_api_utilisateur_id` FOREIGN KEY (`createur_id`) REFERENCES `api_utilisateur` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_information`
--

LOCK TABLES `api_information` WRITE;
/*!40000 ALTER TABLE `api_information` DISABLE KEYS */;
INSERT INTO `api_information` VALUES (1,'Suivez Vos Progrès en Temps Réel','Grâce à votre historique personnalisé, visualisez vos efforts et avancez vers un équilibre durable, jour après jour.','2025-05-26 11:28:55.000000','2025-06-24 19:27:56.935565',1),(2,'Pourquoi la Pause Zen Change Tout','Faire une pause, c’est gagner en clarté mentale. Nos exercices guidés vous aident à retrouver calme et concentration à tout moment de la journée.','2025-05-26 09:31:57.657710','2025-06-24 19:27:37.535992',1),(3,'Découvrez la Respiration Consciente','Apprenez à contrôler votre souffle pour apaiser le stress du quotidien. Quelques minutes par jour suffisent à transformer votre bien-être.','2025-05-26 09:32:12.265975','2025-06-24 19:27:11.829820',1);
/*!40000 ALTER TABLE `api_information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_utilisateur`
--

DROP TABLE IF EXISTS `api_utilisateur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_utilisateur` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `username` varchar(150) NOT NULL,
  `role` varchar(20) NOT NULL,
  `date_inscription` datetime(6) NOT NULL,
  `statut` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_utilisateur`
--

LOCK TABLES `api_utilisateur` WRITE;
/*!40000 ALTER TABLE `api_utilisateur` DISABLE KEYS */;
INSERT INTO `api_utilisateur` VALUES (1,'pbkdf2_sha256$600000$N5fbgwZBlJb2k4vfjFf1ap$bHfHhIzsiEBfC2XF8Yq4IXjEBn9GeDoK4iDtEkzmAyE=','2025-08-31 12:56:46.684412',1,'admin1','nom',1,1,'2025-04-27 17:08:41.522021','bigadmin1@gmail.com','bigadmin1','administrateur','2025-04-27 17:08:41.944251','actif'),(2,'pbkdf2_sha256$600000$MxFOp7UYUUJXXYsBIYz76y$3HrMSgy2MYWgbKC81pUNQ5aYb10btJSmdRHV1St3s6Y=','2025-06-30 13:08:06.799399',0,'prenom1','nom1',0,1,'2025-04-27 17:11:19.000000','test1@gmail.com','test1','utilisateur','2025-04-27 17:11:41.269798','actif'),(3,'pbkdf2_sha256$600000$DERDKjBnBRjkc1twM3B4zM$tGjtrX3q2d0Ud7cA967G2UCjdBwRTii++jdZyxddrqc=',NULL,0,'','',0,1,'2025-06-16 17:21:09.829323','lulubleau@gmail.com','lucas','utilisateur','2025-06-16 17:21:10.275424','actif'),(4,'pbkdf2_sha256$600000$39mxh1pvhNTl861QCYFwts$kJI6gxlw2OHGDqEKXurUn+aZmLRNCwKKSAeKbstT85c=','2025-06-16 17:25:46.379621',0,'essai','essai essai1',0,1,'2025-06-16 17:24:35.364489','essai1@gmail.com','essai1','utilisateur','2025-06-16 17:24:35.804577','actif'),(5,'pbkdf2_sha256$600000$I7wVMmTFOm3htb1ETrxu4M$PAM4RNKyU2xoJuseJacySbG/xDUVFPF1Cqy/21EpwLs=','2025-06-21 15:54:30.835534',0,'','',0,1,'2025-06-21 15:54:29.907035','email.exemple@gmail.com','exemple','utilisateur','2025-06-21 15:54:30.359824','actif'),(6,'pbkdf2_sha256$600000$oec9mh6AGn0wbLIxVPzQMd$tWaoZc8qdW0K3Lg4sPJebbFdVU8JIxSSFanhj3UVZBI=','2025-06-22 12:56:05.933538',0,'','',0,1,'2025-06-21 16:03:43.481545','email@gmail.com','email','utilisateur','2025-06-21 16:03:43.925080','désactivé'),(7,'pbkdf2_sha256$600000$1OOE6g8iYwM5va62DQ00dg$BSdbUWMawoY2AoydQEhVrs4y5UxX6chDw5NpXIhg2Ew=',NULL,0,'','',0,1,'2025-06-21 16:10:35.575304','email2@gmail.com','email2','utilisateur','2025-06-21 16:10:36.021638','actif'),(8,'pbkdf2_sha256$600000$025YN9zxYKALKHuUk5TJVm$xft8oCiSvUyu0qOGYcYggXPNUS5b6xlIHZt9HJ2hJFE=',NULL,0,'','',0,1,'2025-06-21 16:40:00.221826','test48@gmail.com','test48','utilisateur','2025-06-21 16:40:00.664524','actif'),(9,'pbkdf2_sha256$600000$ofMnMlWObyWKL1kHTCpFbu$DGmtm+P9RqiwZRbCUDcx5RfASW+ftie+pywkCVN/oxY=','2025-06-24 16:36:31.875991',0,'','',0,1,'2025-06-24 16:36:30.967641','email90@gmail.com','email90','utilisateur','2025-06-24 16:36:31.424783','actif'),(10,'pbkdf2_sha256$600000$C2D0sE9rhOBBjreWnusFVL$lxqF87SuaetKg7YB5CZoZDdrSkiT0TNQL3Vpjrfry6o=','2025-06-25 16:16:43.591969',0,'prenom','',0,1,'2025-06-25 16:16:42.769034','email144@gmail.com','email144','utilisateur','2025-06-25 16:16:43.181588','désactivé'),(11,'pbkdf2_sha256$600000$nEKfugXeoMFyELraP9zKNt$zeYgLwVf+E2tnWFLJw5hHjgJZZkwCB53eQcx/rqpY9I=','2025-07-01 08:54:41.609317',0,'mat','jean',0,1,'2025-06-30 13:08:35.595585','mat25@gmail.com','mat25','utilisateur','2025-06-30 13:08:36.050266','actif');
/*!40000 ALTER TABLE `api_utilisateur` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_utilisateur_groups`
--

DROP TABLE IF EXISTS `api_utilisateur_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_utilisateur_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `utilisateur_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_utilisateur_groups_utilisateur_id_group_id_1308bcb4_uniq` (`utilisateur_id`,`group_id`),
  KEY `api_utilisateur_groups_group_id_fdf78c4b_fk_auth_group_id` (`group_id`),
  CONSTRAINT `api_utilisateur_grou_utilisateur_id_0caa6b93_fk_api_utili` FOREIGN KEY (`utilisateur_id`) REFERENCES `api_utilisateur` (`id`),
  CONSTRAINT `api_utilisateur_groups_group_id_fdf78c4b_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_utilisateur_groups`
--

LOCK TABLES `api_utilisateur_groups` WRITE;
/*!40000 ALTER TABLE `api_utilisateur_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_utilisateur_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_utilisateur_user_permissions`
--

DROP TABLE IF EXISTS `api_utilisateur_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_utilisateur_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `utilisateur_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_utilisateur_user_per_utilisateur_id_permissio_61068701_uniq` (`utilisateur_id`,`permission_id`),
  KEY `api_utilisateur_user_permission_id_69653c2f_fk_auth_perm` (`permission_id`),
  CONSTRAINT `api_utilisateur_user_permission_id_69653c2f_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `api_utilisateur_user_utilisateur_id_60df7149_fk_api_utili` FOREIGN KEY (`utilisateur_id`) REFERENCES `api_utilisateur` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_utilisateur_user_permissions`
--

LOCK TABLES `api_utilisateur_user_permissions` WRITE;
/*!40000 ALTER TABLE `api_utilisateur_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_utilisateur_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add exercice respiration',6,'add_exercicerespiration'),(22,'Can change exercice respiration',6,'change_exercicerespiration'),(23,'Can delete exercice respiration',6,'delete_exercicerespiration'),(24,'Can view exercice respiration',6,'view_exercicerespiration'),(25,'Can add user',7,'add_utilisateur'),(26,'Can change user',7,'change_utilisateur'),(27,'Can delete user',7,'delete_utilisateur'),(28,'Can view user',7,'view_utilisateur'),(29,'Can add historique exercice',8,'add_historiqueexercice'),(30,'Can change historique exercice',8,'change_historiqueexercice'),(31,'Can delete historique exercice',8,'delete_historiqueexercice'),(32,'Can view historique exercice',8,'view_historiqueexercice'),(33,'Can add information',9,'add_information'),(34,'Can change information',9,'change_information'),(35,'Can delete information',9,'delete_information'),(36,'Can view information',9,'view_information');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_api_utilisateur_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_api_utilisateur_id` FOREIGN KEY (`user_id`) REFERENCES `api_utilisateur` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-04-27 17:11:41.299657','2','test1 (utilisateur)',1,'[{\"added\": {}}]',7,1),(2,'2025-06-24 19:27:11.831114','3','Découvrez la Respiration Consciente',2,'[{\"changed\": {\"fields\": [\"Titre\", \"Contenu\"]}}]',9,1),(3,'2025-06-24 19:27:37.537202','2','Pourquoi la Pause Zen Change Tout',2,'[{\"changed\": {\"fields\": [\"Titre\", \"Contenu\"]}}]',9,1),(4,'2025-06-24 19:27:56.936569','1','Suivez Vos Progrès en Temps Réel',2,'[{\"changed\": {\"fields\": [\"Titre\", \"Contenu\"]}}]',9,1),(5,'2025-07-03 07:45:34.340823','4','<script>alert(\"hello\")</script>',1,'[{\"added\": {}}]',6,1),(6,'2025-08-31 12:56:58.972333','4','<script>alert(\"hello\")</script>',3,'',6,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(6,'api','exercicerespiration'),(8,'api','historiqueexercice'),(9,'api','information'),(7,'api','utilisateur'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-04-27 17:05:24.781517'),(2,'contenttypes','0002_remove_content_type_name','2025-04-27 17:05:24.869942'),(3,'auth','0001_initial','2025-04-27 17:05:25.169477'),(4,'auth','0002_alter_permission_name_max_length','2025-04-27 17:05:25.243330'),(5,'auth','0003_alter_user_email_max_length','2025-04-27 17:05:25.253096'),(6,'auth','0004_alter_user_username_opts','2025-04-27 17:05:25.260093'),(7,'auth','0005_alter_user_last_login_null','2025-04-27 17:05:25.269156'),(8,'auth','0006_require_contenttypes_0002','2025-04-27 17:05:25.273680'),(9,'auth','0007_alter_validators_add_error_messages','2025-04-27 17:05:25.304683'),(10,'auth','0008_alter_user_username_max_length','2025-04-27 17:05:25.313774'),(11,'auth','0009_alter_user_last_name_max_length','2025-04-27 17:05:25.321652'),(12,'auth','0010_alter_group_name_max_length','2025-04-27 17:05:25.335669'),(13,'auth','0011_update_proxy_permissions','2025-04-27 17:05:25.344072'),(14,'auth','0012_alter_user_first_name_max_length','2025-04-27 17:05:25.350069'),(15,'api','0001_initial','2025-04-27 17:05:26.069966'),(16,'admin','0001_initial','2025-04-27 17:05:26.231522'),(17,'admin','0002_logentry_remove_auto_add','2025-04-27 17:05:26.242775'),(18,'admin','0003_logentry_add_action_flag_choices','2025-04-27 17:05:26.253028'),(19,'sessions','0001_initial','2025-04-27 17:05:26.304137');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('624fqgrwbm8atj2xy1hliier77onb9dl','.eJxVi0sKAjEQRO-StQx0_u1OwXOE7qRDgh_EOCvx7kaYhS5qUfXqvVSi9dnSOuSRelF7BWr3uzHls9y-gO592dpYTlfql8N8HTf-JzUabRoYjMvo2aC3UiuDNsAzqAMy-4o6Zx-dJS6QXbEoDkoF0bYEidGr9wfhgjMN:1uWVMY:D9FgOvsKi6sEt5_zaGJaBHPUQXdUXz4bCFOm0M1UfUg','2025-07-15 07:25:06.467496'),('65z5m449qyojmxd69247goo6q6cjyetc','.eJxVi0sKAjEQRO-StQx0_u1OwXOE7qRDgh_EOCvx7kaYhS5qUfXqvVSi9dnSOuSRelF7BWr3uzHls9y-gO592dpYTlfql8N8HTf-JzUabRoYjMvo2aC3UiuDNsAzqAMy-4o6Zx-dJS6QXbEoDkoF0bYEidGr9wfhgjMN:1uJRiE:PcTxPHSU8qpQsbR7-Z9jmCGzk5LlvpedsY74xS6GEz8','2025-06-09 06:53:30.311359'),('8c456ddj4hj8nl2xzmmj7uf513k1gq1y','.eJxVi0sKAjEQRO-StQx0_u1OwXOE7qRDgh_EOCvx7kaYhS5qUfXqvVSi9dnSOuSRelF7BWr3uzHls9y-gO592dpYTlfql8N8HTf-JzUabRoYjMvo2aC3UiuDNsAzqAMy-4o6Zx-dJS6QXbEoDkoF0bYEidGr9wfhgjMN:1uXEQH:qRso33tr8qd7xbxKnYO9rfeUyUByqCM69-5LO3WJtVY','2025-07-17 07:31:57.708415'),('evqqmxp3mw7nol3me0z56k35svk3zk96','.eJxVi0sKAjEQRO-StQx0_u1OwXOE7qRDgh_EOCvx7kaYhS5qUfXqvVSi9dnSOuSRelF7BWr3uzHls9y-gO592dpYTlfql8N8HTf-JzUabRoYjMvo2aC3UiuDNsAzqAMy-4o6Zx-dJS6QXbEoDkoF0bYEidGr9wfhgjMN:1uWX4o:AvZYJbUnK-0HEajBsSA_4Gq2wSdLajuAbioSnFPDobE','2025-07-15 09:14:54.927827'),('fwgo8drxk1g0e96qbcvjxgw1ht2uzex2','.eJxVi0sKAjEQBe-StQz5TTpxp-A5Qne6Q4IfxDgr8e6OMAtdvldVL5Vxeba8DHnkzmqvrNr9foTlLLcvwHuftjWm0xX75bBax43_RQ1HWwsGU5gYoiYHQD5qGyKJ5eREaqoC1TuafawhepBZMJEGzd4U4wNG9f4AA2IzbQ:1uU6ig:nYvMaUnh03xcQ-tw0D7nM0UfnivJKbNmS-sltEQQ0dE','2025-07-08 16:42:02.964561'),('h5k5ztego4d1jiuqmw1zvn4kyk7z4bvc','.eJxVi0sKAjEQBe-StQz5TTpxp-A5Qne6Q4IfxDgr8e6OMAtdvldVL5Vxeba8DHnkzmqvrNr9foTlLLcvwHuftjWm0xX75bBax43_RQ1HWwsGU5gYoiYHQD5qGyKJ5eREaqoC1TuafawhepBZMJEGzd4U4wNG9f4AA2IzbQ:1uW9xj:NA6a7DT60yLKM17BUQUT-MS_BB0_c2lg3-Vh6CF5_fA','2025-07-14 08:34:03.949663'),('hiyj1efrswirandaqkkw8youc7is1sbp','.eJxVi0sKAjEQBe-StQz5TTpxp-A5Qne6Q4IfxDgr8e6OMAtdvldVL5Vxeba8DHnkzmqvrNr9foTlLLcvwHuftjWm0xX75bBax43_RQ1HWwsGU5gYoiYHQD5qGyKJ5eREaqoC1TuafawhepBZMJEGzd4U4wNG9f4AA2IzbQ:1uU6e9:19IiHQnXYcsEHr5YFPH6uWoEFfF_c-9u_piPIlsfh3E','2025-07-08 16:37:21.354526'),('ikstfnk70muedhege4jhf20ck4o2oc7t','.eJxVi0sOwjAMBe-SNarS1HFSdiBxjsh2YiXiI0ToCnF3itQFLN-bmZdJtDxrWnp5pJbN3oDZ_X5Mci63L6B7G7bVh9OV2uWwWseN_0WVel2LjMocNYzAZGckH1yRgshZOQjGkMU6KAWFFaLOFqZJJKqHSN7paN4fIYc0Jw:1uRDac:FQP9SfDpclnRTHVfVyoev_Y4hqlE7foXA_YRACRzEBQ','2025-06-30 17:25:46.383600'),('jg0602py81m2eb75y554dc309q99zlhn','.eJxVi0sKAjEQRO-StQx0_u1OwXOE7qRDgh_EOCvx7kaYhS5qUfXqvVSi9dnSOuSRelF7BWr3uzHls9y-gO592dpYTlfql8N8HTf-JzUabRoYjMvo2aC3UiuDNsAzqAMy-4o6Zx-dJS6QXbEoDkoF0bYEidGr9wfhgjMN:1ushby:MCECa9XgjRYU37tOYCU7ZlHxBzVzr9fwfRmFrqIV-vk','2025-09-14 12:56:46.684412'),('ji1gvrhzyp7qqun3rgtalcbzg31nhqxl','.eJxVi0sKAjEQRO-StQx0_u1OwXOE7qRDgh_EOCvx7kaYhS5qUfXqvVSi9dnSOuSRelF7BWr3uzHls9y-gO592dpYTlfql8N8HTf-JzUabRoYjMvo2aC3UiuDNsAzqAMy-4o6Zx-dJS6QXbEoDkoF0bYEidGr9wfhgjMN:1uTJVn:tQwVsdHZg6-ToGPtXJHAjvgQIlzoLHUNRbAus4SibbE','2025-07-06 12:09:27.004538'),('k7jgyszuwozfmw3r4yoxsuttetubkhum','.eJxVi0sKAjEQBe-StQz5TTpxp-A5Qne6Q4IfxDgr8e6OMAtdvldVL5Vxeba8DHnkzmqvrNr9foTlLLcvwHuftjWm0xX75bBax43_RQ1HWwsGU5gYoiYHQD5qGyKJ5eREaqoC1TuafawhepBZMJEGzd4U4wNG9f4AA2IzbQ:1uU6ez:nB0QTDwya6vI7VyDPhlQfXLOaRnA4oLgJogoNnT8dcY','2025-07-08 16:38:13.965409'),('nrhbeyvqf9usep5lqxcqxxnfh7aghyvh','.eJxVjMsOwiAUBf-FtSEtCNy6dN9vIPcBUjWQ9LEy_rs26UK3Z2bOS0Xc1hK3Jc1xEnVRTp1-N0J-pLoDuWO9Nc2trvNEelf0QRc9NknP6-H-HRRcyrdO0IXgez53ZFjIZKTOIhrrcw9AIOQQPFgv7KCHnAceQBwMAYOzKav3B-y4OCA:1uT0Y2:uaRAZPWvT8ETvZsUjUjfnrpfKq4T3aXlFBPlu9QTyz8','2025-07-05 15:54:30.838017'),('rxa5iw888dswvd2jpk9vjfznwb4bwooj','.eJxVi0sKAjEQRO-StQx0_u1OwXOE7qRDgh_EOCvx7kaYhS5qUfXqvVSi9dnSOuSRelF7BWr3uzHls9y-gO592dpYTlfql8N8HTf-JzUabRoYjMvo2aC3UiuDNsAzqAMy-4o6Zx-dJS6QXbEoDkoF0bYEidGr9wfhgjMN:1uU8KI:f28mH3KbcziwluNw9khqVTSoLXvTxBWeIUoxKLm8fUk','2025-07-08 18:24:58.046444');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-01 18:17:09
