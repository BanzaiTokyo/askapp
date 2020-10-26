-- MySQL dump 10.13  Distrib 5.7.19, for Linux (x86_64)
--
-- Host: localhost    Database: askapp
-- ------------------------------------------------------
-- Server version	5.7.19

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_profile`
--

LOCK TABLES `askapp_profile` WRITE;
/*!40000 ALTER TABLE `askapp_profile` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_userlevel`
--

LOCK TABLES `askapp_userlevel` WRITE;
/*!40000 ALTER TABLE `askapp_userlevel` DISABLE KEYS */;
INSERT INTO `askapp_userlevel` VALUES (1,'Level 1',3,0,1,1);
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can change config',1,'change_config'),(2,'Can view config',1,'view_config'),(3,'Can add constance',2,'add_constance'),(4,'Can change constance',2,'change_constance'),(5,'Can delete constance',2,'delete_constance'),(6,'Can view constance',2,'view_constance'),(7,'Can add Comment',3,'add_post'),(8,'Can change Comment',3,'change_post'),(9,'Can delete Comment',3,'delete_post'),(10,'Can view Comment',3,'view_post'),(11,'Can add tag',4,'add_tag'),(12,'Can change tag',4,'change_tag'),(13,'Can delete tag',4,'delete_tag'),(14,'Can view tag',4,'view_tag'),(15,'Can add action',5,'add_action'),(16,'Can change action',5,'change_action'),(17,'Can delete action',5,'delete_action'),(18,'Can view action',5,'view_action'),(19,'Can add thread',6,'add_thread'),(20,'Can change thread',6,'change_thread'),(21,'Can delete thread',6,'delete_thread'),(22,'Can view thread',6,'view_thread'),(23,'Can add post like',7,'add_postlike'),(24,'Can change post like',7,'change_postlike'),(25,'Can delete post like',7,'delete_postlike'),(26,'Can view post like',7,'view_postlike'),(27,'Can add thread like',8,'add_threadlike'),(28,'Can change thread like',8,'change_threadlike'),(29,'Can delete thread like',8,'delete_threadlike'),(30,'Can view thread like',8,'view_threadlike'),(31,'Can add profile',9,'add_profile'),(32,'Can change profile',9,'change_profile'),(33,'Can delete profile',9,'delete_profile'),(34,'Can view profile',9,'view_profile'),(35,'Can add audit thread',10,'add_auditthread'),(36,'Can change audit thread',10,'change_auditthread'),(37,'Can delete audit thread',10,'delete_auditthread'),(38,'Can view audit thread',10,'view_auditthread'),(39,'Can add user level',11,'add_userlevel'),(40,'Can change user level',11,'change_userlevel'),(41,'Can delete user level',11,'delete_userlevel'),(42,'Can view user level',11,'view_userlevel'),(43,'Can add log entry',12,'add_logentry'),(44,'Can change log entry',12,'change_logentry'),(45,'Can delete log entry',12,'delete_logentry'),(46,'Can view log entry',12,'view_logentry'),(47,'Can add permission',13,'add_permission'),(48,'Can change permission',13,'change_permission'),(49,'Can delete permission',13,'delete_permission'),(50,'Can view permission',13,'view_permission'),(51,'Can add group',14,'add_group'),(52,'Can change group',14,'change_group'),(53,'Can delete group',14,'delete_group'),(54,'Can view group',14,'view_group'),(55,'Can add user',15,'add_user'),(56,'Can change user',15,'change_user'),(57,'Can delete user',15,'delete_user'),(58,'Can view user',15,'view_user'),(59,'Can add content type',16,'add_contenttype'),(60,'Can change content type',16,'change_contenttype'),(61,'Can delete content type',16,'delete_contenttype'),(62,'Can view content type',16,'view_contenttype'),(63,'Can add session',17,'add_session'),(64,'Can change session',17,'change_session'),(65,'Can delete session',17,'delete_session'),(66,'Can view session',17,'view_session'),(67,'Can add registration profile',18,'add_registrationprofile'),(68,'Can change registration profile',18,'change_registrationprofile'),(69,'Can delete registration profile',18,'delete_registrationprofile'),(70,'Can view registration profile',18,'view_registrationprofile'),(71,'Can add supervised registration profile',19,'add_supervisedregistrationprofile'),(72,'Can change supervised registration profile',19,'change_supervisedregistrationprofile'),(73,'Can delete supervised registration profile',19,'delete_supervisedregistrationprofile'),(74,'Can view supervised registration profile',19,'view_supervisedregistrationprofile');
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `constance_config`
--

DROP TABLE IF EXISTS `constance_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `constance_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(255) NOT NULL,
  `value` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `constance_config`
--

LOCK TABLES `constance_config` WRITE;
/*!40000 ALTER TABLE `constance_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `constance_config` ENABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (12,'admin','logentry'),(5,'askapp','action'),(10,'askapp','auditthread'),(3,'askapp','post'),(7,'askapp','postlike'),(9,'askapp','profile'),(4,'askapp','tag'),(6,'askapp','thread'),(8,'askapp','threadlike'),(11,'askapp','userlevel'),(14,'auth','group'),(13,'auth','permission'),(15,'auth','user'),(1,'constance','config'),(16,'contenttypes','contenttype'),(2,'database','constance'),(18,'registration','registrationprofile'),(19,'registration','supervisedregistrationprofile'),(17,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-10-19 18:44:29.498013'),(2,'auth','0001_initial','2020-10-19 18:44:29.686514'),(3,'admin','0001_initial','2020-10-19 18:44:30.118943'),(4,'admin','0002_logentry_remove_auto_add','2020-10-19 18:44:30.368198'),(5,'admin','0003_logentry_add_action_flag_choices','2020-10-19 18:44:30.393353'),(6,'askapp','0001_initial','2020-10-19 18:44:30.861703'),(7,'askapp','0002_thread_thumbnail','2020-10-19 18:44:31.621839'),(8,'askapp','0003_profile','2020-10-19 18:44:31.694615'),(9,'askapp','0004_auto_20161226_1858','2020-10-19 18:44:32.362291'),(10,'askapp','0005_auto_20161227_1123','2020-10-19 18:44:32.835292'),(11,'askapp','0006_post_deleted','2020-10-19 18:44:32.993309'),(12,'askapp','0007_auto_20161228_0818','2020-10-19 18:44:33.104803'),(13,'askapp','0008_auto_20161228_1931','2020-10-19 18:44:33.306440'),(14,'askapp','0009_auto_20170105_1944','2020-10-19 18:44:33.604953'),(15,'askapp','0010_auto_20170106_0657','2020-10-19 18:44:33.633873'),(16,'askapp','0011_auto_20170110_1905','2020-10-19 18:44:33.862168'),(17,'askapp','0012_auto_20170203_1436','2020-10-19 18:44:34.189162'),(18,'askapp','0013_auto_20170206_0748','2020-10-19 18:44:34.333914'),(19,'askapp','0014_auto_20170529_1106','2020-10-19 18:44:34.479691'),(20,'askapp','0015_thread_domain','2020-10-19 18:44:34.545079'),(21,'askapp','0016_populate_domain','2020-10-19 18:44:34.585881'),(22,'askapp','0017_auto_20191105_1229','2020-10-19 18:44:34.689790'),(23,'askapp','0018_auto_20191109_1248','2020-10-19 18:44:34.787174'),(24,'askapp','0019_auto_20191119_0846','2020-10-19 18:44:34.984353'),(25,'contenttypes','0002_remove_content_type_name','2020-10-19 18:44:35.160097'),(26,'auth','0002_alter_permission_name_max_length','2020-10-19 18:44:35.179345'),(27,'auth','0003_alter_user_email_max_length','2020-10-19 18:44:35.219073'),(28,'auth','0004_alter_user_username_opts','2020-10-19 18:44:35.251829'),(29,'auth','0005_alter_user_last_login_null','2020-10-19 18:44:35.345631'),(30,'auth','0006_require_contenttypes_0002','2020-10-19 18:44:35.352210'),(31,'auth','0007_alter_validators_add_error_messages','2020-10-19 18:44:35.387922'),(32,'auth','0008_alter_user_username_max_length','2020-10-19 18:44:35.458015'),(33,'auth','0009_alter_user_last_name_max_length','2020-10-19 18:44:35.500972'),(34,'auth','0010_alter_group_name_max_length','2020-10-19 18:44:35.555464'),(35,'auth','0011_update_proxy_permissions','2020-10-19 18:44:35.656488'),(36,'database','0001_initial','2020-10-19 18:44:35.690086'),(37,'database','0002_auto_20190129_2304','2020-10-19 18:44:35.737402'),(38,'registration','0001_initial','2020-10-19 18:44:35.777032'),(39,'registration','0002_registrationprofile_activated','2020-10-19 18:44:35.893415'),(40,'registration','0003_migrate_activatedstatus','2020-10-19 18:44:35.932093'),(41,'registration','0004_supervisedregistrationprofile','2020-10-19 18:44:35.973952'),(42,'sessions','0001_initial','2020-10-19 18:44:36.041057');
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration_supervisedregistrationprofile`
--

LOCK TABLES `registration_supervisedregistrationprofile` WRITE;
/*!40000 ALTER TABLE `registration_supervisedregistrationprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `registration_supervisedregistrationprofile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-10-19 18:47:04
