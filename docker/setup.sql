-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: 0.0.0.0    Database: askapp
-- ------------------------------------------------------
-- Server version	5.7.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

CREATE DATABASE IF NOT EXISTS `askapp`;
USE `askapp`;

--
-- Table structure for table `askapp_action`
--

DROP TABLE IF EXISTS `askapp_action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `askapp_action` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taken_on` datetime(6) NOT NULL,
  `action_name` longtext NOT NULL,
  `old_text` longtext,
  `old_title` longtext,
  `post_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `askapp_action_post_id_e82b2f1f_fk_askapp_post_id` (`post_id`),
  KEY `askapp_action_user_id_2d4a8b0f_fk_auth_user_id` (`user_id`),
  CONSTRAINT `askapp_action_post_id_e82b2f1f_fk_askapp_post_id` FOREIGN KEY (`post_id`) REFERENCES `askapp_post` (`id`),
  CONSTRAINT `askapp_action_user_id_2d4a8b0f_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_action`
--

LOCK TABLES `askapp_action` WRITE;
/*!40000 ALTER TABLE `askapp_action` DISABLE KEYS */;
/*!40000 ALTER TABLE `askapp_action` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `askapp_auditthread`
--

DROP TABLE IF EXISTS `askapp_auditthread`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `askapp_auditthread` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action` longtext NOT NULL,
  `created` datetime(6) NOT NULL,
  `content` longtext,
  `thread_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `askapp_auditthread_user_id_f0857531_fk_auth_user_id` (`user_id`),
  KEY `askapp_auditthread_thread_id_cfe3ab22_fk_askapp_thread_id` (`thread_id`),
  CONSTRAINT `askapp_auditthread_thread_id_cfe3ab22_fk_askapp_thread_id` FOREIGN KEY (`thread_id`) REFERENCES `askapp_thread` (`id`),
  CONSTRAINT `askapp_auditthread_user_id_f0857531_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_auditthread`
--

LOCK TABLES `askapp_auditthread` WRITE;
/*!40000 ALTER TABLE `askapp_auditthread` DISABLE KEYS */;
/*!40000 ALTER TABLE `askapp_auditthread` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `askapp_post`
--

DROP TABLE IF EXISTS `askapp_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `askapp_post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `text` longtext,
  `is_answer` tinyint(1) NOT NULL,
  `thread_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `level` int(10) unsigned NOT NULL,
  `lft` int(10) unsigned NOT NULL,
  `rght` int(10) unsigned NOT NULL,
  `tree_id` int(10) unsigned NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `accepted` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `askapp_post_thread_id_d9db3a2d_fk_askapp_thread_id` (`thread_id`),
  KEY `askapp_post_user_id_da83df60_fk_auth_user_id` (`user_id`),
  KEY `askapp_post_parent_id_904a68f7_fk_askapp_post_id` (`parent_id`),
  KEY `askapp_post_level_e3e8ec09` (`level`),
  KEY `askapp_post_lft_e5469fbc` (`lft`),
  KEY `askapp_post_rght_c426b3ee` (`rght`),
  KEY `askapp_post_tree_id_0be5a134` (`tree_id`),
  CONSTRAINT `askapp_post_parent_id_904a68f7_fk_askapp_post_id` FOREIGN KEY (`parent_id`) REFERENCES `askapp_post` (`id`),
  CONSTRAINT `askapp_post_thread_id_d9db3a2d_fk_askapp_thread_id` FOREIGN KEY (`thread_id`) REFERENCES `askapp_thread` (`id`),
  CONSTRAINT `askapp_post_user_id_da83df60_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_post`
--

LOCK TABLES `askapp_post` WRITE;
/*!40000 ALTER TABLE `askapp_post` DISABLE KEYS */;
/*!40000 ALTER TABLE `askapp_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `askapp_postlike`
--

DROP TABLE IF EXISTS `askapp_postlike`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `askapp_postlike` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `points` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `askapp_postlike_user_id_5dc04ebc_fk_auth_user_id` (`user_id`),
  KEY `askapp_postlike_post_id_c7c2d1ea_fk_askapp_post_id` (`post_id`),
  CONSTRAINT `askapp_postlike_post_id_c7c2d1ea_fk_askapp_post_id` FOREIGN KEY (`post_id`) REFERENCES `askapp_post` (`id`),
  CONSTRAINT `askapp_postlike_user_id_5dc04ebc_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_postlike`
--

LOCK TABLES `askapp_postlike` WRITE;
/*!40000 ALTER TABLE `askapp_postlike` DISABLE KEYS */;
/*!40000 ALTER TABLE `askapp_postlike` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `askapp_profile`
--

DROP TABLE IF EXISTS `askapp_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `askapp_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `avatar` varchar(100) NOT NULL,
  `country` varchar(2) NOT NULL,
  `city` varchar(50) NOT NULL,
  `about` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  `level_id` int(11),
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `askapp_profile_level_id_ab8f8537_fk_askapp_userlevel_id` (`level_id`),
  CONSTRAINT `askapp_profile_level_id_ab8f8537_fk_askapp_userlevel_id` FOREIGN KEY (`level_id`) REFERENCES `askapp_userlevel` (`id`),
  CONSTRAINT `askapp_profile_user_id_d55e2c5d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_profile`
--

LOCK TABLES `askapp_profile` WRITE;
/*!40000 ALTER TABLE `askapp_profile` DISABLE KEYS */;
REPLACE INTO `askapp_profile` (`id`, `avatar`, `country`, `city`, `about`, `user_id`, `level_id`) VALUES (1,'','','','',1,1);
/*!40000 ALTER TABLE `askapp_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `askapp_tag`
--

DROP TABLE IF EXISTS `askapp_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `askapp_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) NOT NULL,
  `slug` varchar(60) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `askapp_tag_slug_85920a06` (`slug`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_tag`
--

LOCK TABLES `askapp_tag` WRITE;
/*!40000 ALTER TABLE `askapp_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `askapp_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `askapp_thread`
--

DROP TABLE IF EXISTS `askapp_thread`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `askapp_thread` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hidden` tinyint(1) NOT NULL,
  `closed` tinyint(1) NOT NULL,
  `sticky` date DEFAULT NULL,
  `featured` tinyint(1) NOT NULL,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `thread_type` varchar(2) DEFAULT NULL,
  `text` longtext,
  `title` varchar(255) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `score` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `link` varchar(200) DEFAULT NULL,
  `thumbnail` varchar(100) DEFAULT NULL,
  `deleted` tinyint(1) NOT NULL,
  `domain` varchar(255) DEFAULT NULL,
  `original_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `askapp_thread_link_cab6fd3a_uniq` (`link`),
  KEY `askapp_thread_user_id_e7f37374_fk_auth_user_id` (`user_id`),
  KEY `askapp_thread_original_id_87c0a1ba_fk_askapp_thread_id` (`original_id`),
  CONSTRAINT `askapp_thread_original_id_87c0a1ba_fk_askapp_thread_id` FOREIGN KEY (`original_id`) REFERENCES `askapp_thread` (`id`),
  CONSTRAINT `askapp_thread_user_id_e7f37374_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_thread`
--

LOCK TABLES `askapp_thread` WRITE;
/*!40000 ALTER TABLE `askapp_thread` DISABLE KEYS */;
/*!40000 ALTER TABLE `askapp_thread` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `askapp_thread_tags`
--

DROP TABLE IF EXISTS `askapp_thread_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `askapp_thread_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `thread_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `askapp_thread_tags_thread_id_tag_id_995ef60a_uniq` (`thread_id`,`tag_id`),
  KEY `askapp_thread_tags_tag_id_09eae662_fk_askapp_tag_id` (`tag_id`),
  CONSTRAINT `askapp_thread_tags_tag_id_09eae662_fk_askapp_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `askapp_tag` (`id`),
  CONSTRAINT `askapp_thread_tags_thread_id_46786677_fk_askapp_thread_id` FOREIGN KEY (`thread_id`) REFERENCES `askapp_thread` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_thread_tags`
--

LOCK TABLES `askapp_thread_tags` WRITE;
/*!40000 ALTER TABLE `askapp_thread_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `askapp_thread_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `askapp_threadlike`
--

DROP TABLE IF EXISTS `askapp_threadlike`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `askapp_threadlike` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `points` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `thread_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `askapp_threadlike_user_id_359acf5e_fk_auth_user_id` (`user_id`),
  KEY `askapp_threadlike_thread_id_f6ffde17_fk_askapp_thread_id` (`thread_id`),
  CONSTRAINT `askapp_threadlike_thread_id_f6ffde17_fk_askapp_thread_id` FOREIGN KEY (`thread_id`) REFERENCES `askapp_thread` (`id`),
  CONSTRAINT `askapp_threadlike_user_id_359acf5e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_threadlike`
--

LOCK TABLES `askapp_threadlike` WRITE;
/*!40000 ALTER TABLE `askapp_threadlike` DISABLE KEYS */;
/*!40000 ALTER TABLE `askapp_threadlike` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `askapp_userlevel`
--

DROP TABLE IF EXISTS `askapp_userlevel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `askapp_userlevel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `upvotes` int(11) NOT NULL,
  `downvotes` int(11) NOT NULL,
  `upvote_same` int(11) NOT NULL,
  `downvote_same` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_userlevel`
--

LOCK TABLES `askapp_userlevel` WRITE;
/*!40000 ALTER TABLE `askapp_userlevel` DISABLE KEYS */;
REPLACE INTO `askapp_userlevel` (`id`, `name`, `upvotes`, `downvotes`, `upvote_same`, `downvote_same`) VALUES (1,'Level 1',3,0,1,1);
/*!40000 ALTER TABLE `askapp_userlevel` ENABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
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
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
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
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
REPLACE INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (1,'Can add Preference',1,'add_preference'),(2,'Can change Preference',1,'change_preference'),(3,'Can delete Preference',1,'delete_preference'),(4,'Can view Preference',1,'view_preference'),(5,'Can add Comment',2,'add_post'),(6,'Can change Comment',2,'change_post'),(7,'Can delete Comment',2,'delete_post'),(8,'Can view Comment',2,'view_post'),(9,'Can add tag',3,'add_tag'),(10,'Can change tag',3,'change_tag'),(11,'Can delete tag',3,'delete_tag'),(12,'Can view tag',3,'view_tag'),(13,'Can add action',4,'add_action'),(14,'Can change action',4,'change_action'),(15,'Can delete action',4,'delete_action'),(16,'Can view action',4,'view_action'),(17,'Can add thread',5,'add_thread'),(18,'Can change thread',5,'change_thread'),(19,'Can delete thread',5,'delete_thread'),(20,'Can view thread',5,'view_thread'),(21,'Can add post like',6,'add_postlike'),(22,'Can change post like',6,'change_postlike'),(23,'Can delete post like',6,'delete_postlike'),(24,'Can view post like',6,'view_postlike'),(25,'Can add thread like',7,'add_threadlike'),(26,'Can change thread like',7,'change_threadlike'),(27,'Can delete thread like',7,'delete_threadlike'),(28,'Can view thread like',7,'view_threadlike'),(29,'Can add profile',8,'add_profile'),(30,'Can change profile',8,'change_profile'),(31,'Can delete profile',8,'delete_profile'),(32,'Can view profile',8,'view_profile'),(33,'Can add audit thread',9,'add_auditthread'),(34,'Can change audit thread',9,'change_auditthread'),(35,'Can delete audit thread',9,'delete_auditthread'),(36,'Can view audit thread',9,'view_auditthread'),(37,'Can add user level',10,'add_userlevel'),(38,'Can change user level',10,'change_userlevel'),(39,'Can delete user level',10,'delete_userlevel'),(40,'Can view user level',10,'view_userlevel'),(41,'Can add log entry',11,'add_logentry'),(42,'Can change log entry',11,'change_logentry'),(43,'Can delete log entry',11,'delete_logentry'),(44,'Can view log entry',11,'view_logentry'),(45,'Can add permission',12,'add_permission'),(46,'Can change permission',12,'change_permission'),(47,'Can delete permission',12,'delete_permission'),(48,'Can view permission',12,'view_permission'),(49,'Can add group',13,'add_group'),(50,'Can change group',13,'change_group'),(51,'Can delete group',13,'delete_group'),(52,'Can view group',13,'view_group'),(53,'Can add user',14,'add_user'),(54,'Can change user',14,'change_user'),(55,'Can delete user',14,'delete_user'),(56,'Can view user',14,'view_user'),(57,'Can add content type',15,'add_contenttype'),(58,'Can change content type',15,'change_contenttype'),(59,'Can delete content type',15,'delete_contenttype'),(60,'Can view content type',15,'view_contenttype'),(61,'Can add session',16,'add_session'),(62,'Can change session',16,'change_session'),(63,'Can delete session',16,'delete_session'),(64,'Can view session',16,'view_session'),(65,'Can add registration profile',17,'add_registrationprofile'),(66,'Can change registration profile',17,'change_registrationprofile'),(67,'Can delete registration profile',17,'delete_registrationprofile'),(68,'Can view registration profile',17,'view_registrationprofile'),(69,'Can add supervised registration profile',18,'add_supervisedregistrationprofile'),(70,'Can change supervised registration profile',18,'change_supervisedregistrationprofile'),(71,'Can delete supervised registration profile',18,'delete_supervisedregistrationprofile'),(72,'Can view supervised registration profile',18,'view_supervisedregistrationprofile');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
REPLACE INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES (1,'pbkdf2_sha256$150000$7YO0IhWrnNGW$r2KhVW5tickuP9JoRaeOZvRhiqUZK7QPPtKksuuIkSU=',NULL,1,'askapp','','','askapp@askapp.com',1,1,'2020-09-26 22:06:39.198823');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
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
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
REPLACE INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (11,'admin','logentry'),(4,'askapp','action'),(9,'askapp','auditthread'),(2,'askapp','post'),(6,'askapp','postlike'),(8,'askapp','profile'),(3,'askapp','tag'),(5,'askapp','thread'),(7,'askapp','threadlike'),(10,'askapp','userlevel'),(13,'auth','group'),(12,'auth','permission'),(14,'auth','user'),(15,'contenttypes','contenttype'),(17,'registration','registrationprofile'),(18,'registration','supervisedregistrationprofile'),(16,'sessions','session'),(1,'siteprefs','preference');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
REPLACE INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (1,'contenttypes','0001_initial','2020-09-26 21:58:28.528476'),(2,'auth','0001_initial','2020-09-26 21:58:29.025619'),(3,'admin','0001_initial','2020-09-26 21:58:29.659220'),(4,'admin','0002_logentry_remove_auto_add','2020-09-26 21:58:29.755076'),(5,'admin','0003_logentry_add_action_flag_choices','2020-09-26 21:58:29.768123'),(6,'askapp','0001_initial','2020-09-26 21:58:30.246910'),(7,'askapp','0002_thread_thumbnail','2020-09-26 21:58:30.695898'),(8,'askapp','0003_profile','2020-09-26 21:58:30.750171'),(9,'askapp','0004_auto_20161226_1858','2020-09-26 21:58:31.320132'),(10,'askapp','0005_auto_20161227_1123','2020-09-26 21:58:31.853940'),(11,'askapp','0006_post_deleted','2020-09-26 21:58:32.031575'),(12,'askapp','0007_auto_20161228_0818','2020-09-26 21:58:32.123546'),(13,'askapp','0008_auto_20161228_1931','2020-09-26 21:58:32.395629'),(14,'askapp','0009_auto_20170105_1944','2020-09-26 21:58:32.606420'),(15,'askapp','0010_auto_20170106_0657','2020-09-26 21:58:32.637783'),(16,'askapp','0011_auto_20170110_1905','2020-09-26 21:58:32.888390'),(17,'askapp','0012_auto_20170203_1436','2020-09-26 21:58:33.223488'),(18,'askapp','0013_auto_20170206_0748','2020-09-26 21:58:33.338845'),(19,'askapp','0014_auto_20170529_1106','2020-09-26 21:58:33.474184'),(20,'askapp','0015_thread_domain','2020-09-26 21:58:33.544614'),(21,'askapp','0016_populate_domain','2020-09-26 21:58:33.574611'),(22,'askapp','0017_auto_20191105_1229','2020-09-26 21:58:33.669750'),(23,'askapp','0018_auto_20191109_1248','2020-09-26 21:58:33.765568'),(24,'askapp','0019_auto_20191119_0846','2020-09-26 21:58:33.943705'),(25,'contenttypes','0002_remove_content_type_name','2020-09-26 21:58:34.110056'),(26,'auth','0002_alter_permission_name_max_length','2020-09-26 21:58:34.143061'),(27,'auth','0003_alter_user_email_max_length','2020-09-26 21:58:34.193309'),(28,'auth','0004_alter_user_username_opts','2020-09-26 21:58:34.223287'),(29,'auth','0005_alter_user_last_login_null','2020-09-26 21:58:34.268763'),(30,'auth','0006_require_contenttypes_0002','2020-09-26 21:58:34.271412'),(31,'auth','0007_alter_validators_add_error_messages','2020-09-26 21:58:34.295259'),(32,'auth','0008_alter_user_username_max_length','2020-09-26 21:58:34.374245'),(33,'auth','0009_alter_user_last_name_max_length','2020-09-26 21:58:34.520196'),(34,'auth','0010_alter_group_name_max_length','2020-09-26 21:58:34.561457'),(35,'auth','0011_update_proxy_permissions','2020-09-26 21:58:34.602354'),(36,'registration','0001_initial','2020-09-26 21:58:34.645033'),(37,'registration','0002_registrationprofile_activated','2020-09-26 21:58:34.732076'),(38,'registration','0003_migrate_activatedstatus','2020-09-26 21:58:34.762271'),(39,'registration','0004_supervisedregistrationprofile','2020-09-26 21:58:34.798096'),(40,'sessions','0001_initial','2020-09-26 21:58:34.869995'),(41,'siteprefs','0001_initial','2020-09-26 21:58:34.955206');
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration_registrationprofile`
--

DROP TABLE IF EXISTS `registration_registrationprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registration_registrationprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `activation_key` varchar(40) NOT NULL,
  `user_id` int(11) NOT NULL,
  `activated` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `registration_registr_user_id_5fcbf725_fk_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration_registrationprofile`
--

LOCK TABLES `registration_registrationprofile` WRITE;
/*!40000 ALTER TABLE `registration_registrationprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `registration_registrationprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration_supervisedregistrationprofile`
--

DROP TABLE IF EXISTS `registration_supervisedregistrationprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registration_supervisedregistrationprofile` (
  `registrationprofile_ptr_id` int(11) NOT NULL,
  PRIMARY KEY (`registrationprofile_ptr_id`),
  CONSTRAINT `registration_supervi_registrationprofile__0a59f3b2_fk_registrat` FOREIGN KEY (`registrationprofile_ptr_id`) REFERENCES `registration_registrationprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration_supervisedregistrationprofile`
--

LOCK TABLES `registration_supervisedregistrationprofile` WRITE;
/*!40000 ALTER TABLE `registration_supervisedregistrationprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `registration_supervisedregistrationprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `siteprefs_preference`
--

DROP TABLE IF EXISTS `siteprefs_preference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `siteprefs_preference` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(100) DEFAULT NULL,
  `name` varchar(150) NOT NULL,
  `text` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `siteprefs_preference_app_name_77aef2db_uniq` (`app`,`name`),
  KEY `siteprefs_preference_app_95cca980` (`app`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `siteprefs_preference`
--

LOCK TABLES `siteprefs_preference` WRITE;
/*!40000 ALTER TABLE `siteprefs_preference` DISABLE KEYS */;
/*!40000 ALTER TABLE `siteprefs_preference` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-09-27  1:07:47
