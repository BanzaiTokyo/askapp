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
-- Table structure for table `account_emailaddress`
--

DROP TABLE IF EXISTS `account_emailaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_emailaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `account_emailaddress_user_id_2c513194_fk_auth_user_id` (`user_id`),
  CONSTRAINT `account_emailaddress_user_id_2c513194_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailaddress`
--

LOCK TABLES `account_emailaddress` WRITE;
/*!40000 ALTER TABLE `account_emailaddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_emailconfirmation`
--

DROP TABLE IF EXISTS `account_emailconfirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_emailconfirmation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) NOT NULL,
  `email_address_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` (`email_address_id`),
  CONSTRAINT `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailconfirmation`
--

LOCK TABLES `account_emailconfirmation` WRITE;
/*!40000 ALTER TABLE `account_emailconfirmation` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailconfirmation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `askapp_auditmodel`
--

DROP TABLE IF EXISTS `askapp_auditmodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `askapp_auditmodel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_auditmodel`
--

LOCK TABLES `askapp_auditmodel` WRITE;
/*!40000 ALTER TABLE `askapp_auditmodel` DISABLE KEYS */;
/*!40000 ALTER TABLE `askapp_auditmodel` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_auditthread`
--

LOCK TABLES `askapp_auditthread` WRITE;
/*!40000 ALTER TABLE `askapp_auditthread` DISABLE KEYS */;
INSERT INTO `askapp_auditthread` VALUES (1,'sticky','2020-10-18 20:57:27.423467',NULL,3,1);
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
  KEY `askapp_post_tree_id_0be5a134` (`tree_id`),
  CONSTRAINT `askapp_post_parent_id_904a68f7_fk_askapp_post_id` FOREIGN KEY (`parent_id`) REFERENCES `askapp_post` (`id`),
  CONSTRAINT `askapp_post_thread_id_d9db3a2d_fk_askapp_thread_id` FOREIGN KEY (`thread_id`) REFERENCES `askapp_thread` (`id`),
  CONSTRAINT `askapp_post_user_id_da83df60_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_post`
--

LOCK TABLES `askapp_post` WRITE;
/*!40000 ALTER TABLE `askapp_post` DISABLE KEYS */;
INSERT INTO `askapp_post` VALUES (1,'2020-10-18 19:22:21.452923',NULL,'Thanks for your interest in AskApp. We also believe that it is a nice content management tool. Unfortunately we haven\'t written a comprehensive documentation where you can learn about everything AskApp can do. But this is how Open Source works - if you see something is missing in a repository, feel free to contribute. If you are not interested in writing the doc yourself, you can post an issue in the repository. That way we\'ll know what exactly you need and we\'ll do our best to help. Isues motivate us to move forward.',0,6,1,0,1,4,1,0,NULL),(2,'2020-10-18 19:28:51.228877',1,'This is nice to hear, I will check out AskApp repository and see how I could contribute!',0,6,4,1,2,3,1,0,NULL),(3,'2020-10-18 20:58:01.809000',NULL,'Why is this article highlighted?',0,3,1,0,1,4,2,0,NULL),(4,'2020-10-18 20:59:16.800263',3,'I am glad you have asked! In the admin panel you can choose to make any document sticky. It will make the document appear at the top of the feed for the duration of time you chose for it to be sticky. You can program the document to be sticky for any duration. Once the period expired, the document will return to being normal.',0,3,4,1,2,3,2,0,NULL);
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
  `level_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `askapp_profile_level_id_ab8f8537_fk_askapp_userlevel_id` (`level_id`),
  CONSTRAINT `askapp_profile_level_id_ab8f8537_fk_askapp_userlevel_id` FOREIGN KEY (`level_id`) REFERENCES `askapp_userlevel` (`id`),
  CONSTRAINT `askapp_profile_user_id_d55e2c5d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_profile`
--

LOCK TABLES `askapp_profile` WRITE;
/*!40000 ALTER TABLE `askapp_profile` DISABLE KEYS */;
INSERT INTO `askapp_profile` VALUES (1,'user_profile/askapp1.jpg','FR','Toulouse','I am a testing admin account. My password is my username. The same as for all other test users.',1,1),(4,'user_profile/RamenRyan3.jpg','KH','Phnom Penh','I am a test user, I don\'t really live in Cambodia.',3,1),(5,'user_profile/SobaSmith4.jpg','GB','London','I am a test user. I don\'t exist in real life.',4,1),(6,'user_profile/CarlosYuzu5.jpg','AR','Buenos Aires','I am just a test user',5,1),(7,'user_profile/BarbaraEbara6.jpg','JP','Toyama','I am a test user, I don\'t exist in real life. But Ebara exists. It is a tiny train station near Toyama city in Japan.',6,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_tag`
--

LOCK TABLES `askapp_tag` WRITE;
/*!40000 ALTER TABLE `askapp_tag` DISABLE KEYS */;
INSERT INTO `askapp_tag` VALUES (1,'AskApp','askapp'),(2,'Example','example'),(3,'FunFact','funfact');
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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_thread`
--

LOCK TABLES `askapp_thread` WRITE;
/*!40000 ALTER TABLE `askapp_thread` DISABLE KEYS */;
INSERT INTO `askapp_thread` VALUES (1,0,0,NULL,0,'2020-10-18 18:49:39.287907','2020-10-18 18:49:39.287950','DD','Here\'s a photo of a web sloth. Because why not. You can use AskApp for any content.','Wet Sloth','uploads/images/2020/10/18/wet_sloth.jpg',0,5,NULL,'',0,NULL,NULL),(2,0,0,NULL,0,'2020-10-18 18:53:09.540153','2020-10-18 18:53:09.540200','YT','There is a YouTube video type of document in AskApp. You can just paste the YouTube URL and click \"Preload\" button and it will pull the video\'s description from youtube that you can later modify.','PSY - GANGNAM STYLE','uploads/images/2020/10/18/9bZkp7q19f0.jpg',0,5,'https://www.youtube.com/watch?v=9bZkp7q19f0','',0,NULL,NULL),(3,0,0,'2021-10-26',0,'2020-10-18 18:54:19.988537','2020-10-18 20:57:27.421241','DD','The main feature of AskApp is content curation. Much like HackerNews or Reddit, the articles posted here are displayed in a chronological order and the top page features the most upvoted articles with the priority given to more recent posts.','What is AskApp About?','',2,4,NULL,'',0,NULL,NULL),(4,0,0,NULL,0,'2020-10-18 19:10:08.782238','2020-10-18 20:54:48.837363','LL','It is a showcase website for AspApp. It collects and curates articles about Japan. You can find all types of documents - Links, Discussions, YouTube videos.','Akihabara.Tokyo','uploads/images/2020/10/18/largelogo_6l3yibd.jpg',1,4,'https://akihabara.tokyo','',0,'akihabara.tokyo',NULL),(5,0,0,NULL,1,'2020-10-18 19:21:10.659009','2020-10-18 19:24:43.658746','DD','This is an example of a featured document. It doesn\'t matter what type it is, it can be a Link, a Discussion or a YouTube video. The point of being featured is that it will appear in the feed  highlighted. Unlike a Sticky document, it will not remain at the top of the feed, but will be pushed down in the Recent feed as new documents are added. It may or may not get featured on the Top page  depending on the number of upvotes it gets, just like any other document.','This is a Featured Document','',0,3,NULL,'',0,NULL,NULL),(6,0,0,NULL,0,'2020-10-18 19:21:52.418147','2020-10-18 19:21:52.418182','DD','AskApp looks cool and I would be interested in using it, but I can\'t seem to find complete documentation. I wish there was a place where I could read about all the features.','I wish there was a more complete documentation','',0,3,NULL,'',0,NULL,NULL),(7,0,0,NULL,0,'2020-10-18 19:36:43.119561','2020-10-18 19:36:43.119597','LL','AskApp is the content curation and community building system. It is simple, yet flexible. If you are reading this you have already cloned the code from the repository and even managed to run the dockerezed version locally. Great job!','Here\'s AskApp code repository','',0,1,'https://github.com/BanzaiTokyo/askapp','',0,'github.com',NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_thread_tags`
--

LOCK TABLES `askapp_thread_tags` WRITE;
/*!40000 ALTER TABLE `askapp_thread_tags` DISABLE KEYS */;
INSERT INTO `askapp_thread_tags` VALUES (1,1,3),(2,2,3),(3,3,1),(4,4,1),(5,5,1),(6,6,1),(7,7,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `askapp_threadlike`
--

LOCK TABLES `askapp_threadlike` WRITE;
/*!40000 ALTER TABLE `askapp_threadlike` DISABLE KEYS */;
INSERT INTO `askapp_threadlike` VALUES (1,'2020-10-18 19:19:27.714051',2,1,3),(2,'2020-10-18 19:19:29.396234',1,1,4);
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
) ENGINE=InnoDB AUTO_INCREMENT=111 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add Preference',1,'add_preference'),(2,'Can change Preference',1,'change_preference'),(3,'Can delete Preference',1,'delete_preference'),(4,'Can view Preference',1,'view_preference'),(5,'Can add Comment',2,'add_post'),(6,'Can change Comment',2,'change_post'),(7,'Can delete Comment',2,'delete_post'),(8,'Can view Comment',2,'view_post'),(9,'Can add tag',3,'add_tag'),(10,'Can change tag',3,'change_tag'),(11,'Can delete tag',3,'delete_tag'),(12,'Can view tag',3,'view_tag'),(13,'Can add action',4,'add_action'),(14,'Can change action',4,'change_action'),(15,'Can delete action',4,'delete_action'),(16,'Can view action',4,'view_action'),(17,'Can add thread',5,'add_thread'),(18,'Can change thread',5,'change_thread'),(19,'Can delete thread',5,'delete_thread'),(20,'Can view thread',5,'view_thread'),(21,'Can add post like',6,'add_postlike'),(22,'Can change post like',6,'change_postlike'),(23,'Can delete post like',6,'delete_postlike'),(24,'Can view post like',6,'view_postlike'),(25,'Can add thread like',7,'add_threadlike'),(26,'Can change thread like',7,'change_threadlike'),(27,'Can delete thread like',7,'delete_threadlike'),(28,'Can view thread like',7,'view_threadlike'),(29,'Can add profile',8,'add_profile'),(30,'Can change profile',8,'change_profile'),(31,'Can delete profile',8,'delete_profile'),(32,'Can view profile',8,'view_profile'),(33,'Can add audit thread',9,'add_auditthread'),(34,'Can change audit thread',9,'change_auditthread'),(35,'Can delete audit thread',9,'delete_auditthread'),(36,'Can view audit thread',9,'view_auditthread'),(37,'Can add user level',10,'add_userlevel'),(38,'Can change user level',10,'change_userlevel'),(39,'Can delete user level',10,'delete_userlevel'),(40,'Can view user level',10,'view_userlevel'),(41,'Can add log entry',11,'add_logentry'),(42,'Can change log entry',11,'change_logentry'),(43,'Can delete log entry',11,'delete_logentry'),(44,'Can view log entry',11,'view_logentry'),(45,'Can add permission',12,'add_permission'),(46,'Can change permission',12,'change_permission'),(47,'Can delete permission',12,'delete_permission'),(48,'Can view permission',12,'view_permission'),(49,'Can add group',13,'add_group'),(50,'Can change group',13,'change_group'),(51,'Can delete group',13,'delete_group'),(52,'Can view group',13,'view_group'),(53,'Can add user',14,'add_user'),(54,'Can change user',14,'change_user'),(55,'Can delete user',14,'delete_user'),(56,'Can view user',14,'view_user'),(57,'Can add content type',15,'add_contenttype'),(58,'Can change content type',15,'change_contenttype'),(59,'Can delete content type',15,'delete_contenttype'),(60,'Can view content type',15,'view_contenttype'),(61,'Can add session',16,'add_session'),(62,'Can change session',16,'change_session'),(63,'Can delete session',16,'delete_session'),(64,'Can view session',16,'view_session'),(65,'Can add registration profile',17,'add_registrationprofile'),(66,'Can change registration profile',17,'change_registrationprofile'),(67,'Can delete registration profile',17,'delete_registrationprofile'),(68,'Can view registration profile',17,'view_registrationprofile'),(69,'Can add supervised registration profile',18,'add_supervisedregistrationprofile'),(70,'Can change supervised registration profile',18,'change_supervisedregistrationprofile'),(71,'Can delete supervised registration profile',18,'delete_supervisedregistrationprofile'),(72,'Can view supervised registration profile',18,'view_supervisedregistrationprofile'),(73,'Can change config',19,'change_config'),(74,'Can view config',19,'view_config'),(75,'Can add constance',20,'add_constance'),(76,'Can change constance',20,'change_constance'),(77,'Can delete constance',20,'delete_constance'),(78,'Can view constance',20,'view_constance'),(79,'Can add audit model',21,'add_auditmodel'),(80,'Can change audit model',21,'change_auditmodel'),(81,'Can delete audit model',21,'delete_auditmodel'),(82,'Can view audit model',21,'view_auditmodel'),(83,'Can add log entry',22,'add_logentry'),(84,'Can change log entry',22,'change_logentry'),(85,'Can delete log entry',22,'delete_logentry'),(86,'Can view log entry',22,'view_logentry'),(87,'Can add site',23,'add_site'),(88,'Can change site',23,'change_site'),(89,'Can delete site',23,'delete_site'),(90,'Can view site',23,'view_site'),(91,'Can add email address',24,'add_emailaddress'),(92,'Can change email address',24,'change_emailaddress'),(93,'Can delete email address',24,'delete_emailaddress'),(94,'Can view email address',24,'view_emailaddress'),(95,'Can add email confirmation',25,'add_emailconfirmation'),(96,'Can change email confirmation',25,'change_emailconfirmation'),(97,'Can delete email confirmation',25,'delete_emailconfirmation'),(98,'Can view email confirmation',25,'view_emailconfirmation'),(99,'Can add social account',26,'add_socialaccount'),(100,'Can change social account',26,'change_socialaccount'),(101,'Can delete social account',26,'delete_socialaccount'),(102,'Can view social account',26,'view_socialaccount'),(103,'Can add social application',27,'add_socialapp'),(104,'Can change social application',27,'change_socialapp'),(105,'Can delete social application',27,'delete_socialapp'),(106,'Can view social application',27,'view_socialapp'),(107,'Can add social application token',28,'add_socialtoken'),(108,'Can change social application token',28,'change_socialtoken'),(109,'Can delete social application token',28,'delete_socialtoken'),(110,'Can view social application token',28,'view_socialtoken');
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
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$7YO0IhWrnNGW$r2KhVW5tickuP9JoRaeOZvRhiqUZK7QPPtKksuuIkSU=','2020-10-19 19:18:50.340697',1,'askapp','','','askapp@askapp.com',1,1,'2020-09-26 22:06:39.198823'),(3,'pbkdf2_sha256$150000$fwFqzKH9ROrI$H3cW69NtUf3uQ9tk6RygKZ9iau4jCnywoZoTGrZrdxk=','2020-10-18 19:29:12.928720',0,'RamenRyan','','','',0,1,'2020-10-18 18:20:46.207807'),(4,'pbkdf2_sha256$150000$qN4UDoyLPglg$avwS2tIA6jtvjBa4w9BbwoMeasBMYtFtWUdZwdlJQTY=','2020-10-18 20:58:18.611945',0,'SobaSmith','','','',0,1,'2020-10-18 18:22:07.327790'),(5,'pbkdf2_sha256$150000$ZbkgNqo5dtme$US5eysEmoevtEUFaGa5Hej3aho90R2oRcRVJoPH7Ra8=','2020-10-18 18:49:12.304445',0,'CarlosYuzu','','','',0,1,'2020-10-18 18:22:38.357723'),(6,'pbkdf2_sha256$150000$QsQDnp8hodS1$c+zktvRPM5UOBlQ7zCppektCOBhCelaFKWZqbfPTTbM=','2020-10-18 19:30:36.986458',0,'BarbaraEbara','','','',0,1,'2020-10-18 18:23:48.997651');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `constance_config`
--

LOCK TABLES `constance_config` WRITE;
/*!40000 ALTER TABLE `constance_config` DISABLE KEYS */;
INSERT INTO `constance_config` VALUES (1,'SITE_LOGO','gAJYDgAAAHRleHRidWJibGUucG5ncQAu'),(2,'SITE_NAME','gAJYCwAAAEFza0FwcCBEZW1vcQAu'),(3,'ABOUT_TEXT','gAJYywAAAFRoaXMgaXMgYSBkZW1vbnN0cmF0aW9uIHZlcnNpb24gb2YgQXNrQXBwLiBBbGwgdGhlIHRlc3QgdXNlcnMgaGF2ZSB0aGVpciB1c2VybmFtZXMgYXMgcGFzc3dvcmRzLCBleGFtcGxlOiBhc2thcHAvYXNrYXBwIFRoaXMgZGVzY3JpcHRpb24gaXMgZWRpdGFibGUgaW4gdGhlIGNvbnRyb2wgcGFuZWwgYXQgbG9jYWxob3N0OjgwMDAvYWRtaW4gPT4gQ29uZmlncQAu'),(4,'REGISTRATION_OPEN','gAKILg=='),(5,'NUM_DOMAIN_STATS','gAJLMi4=');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2020-10-18 18:20:46.363205','3','RamenRyan',1,'[{\"added\": {}}]',14,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (24,'account','emailaddress'),(25,'account','emailconfirmation'),(22,'admin','logentry'),(4,'askapp','action'),(21,'askapp','auditmodel'),(9,'askapp','auditthread'),(2,'askapp','post'),(6,'askapp','postlike'),(8,'askapp','profile'),(3,'askapp','tag'),(5,'askapp','thread'),(7,'askapp','threadlike'),(10,'askapp','userlevel'),(13,'auth','group'),(12,'auth','permission'),(14,'auth','user'),(19,'constance','config'),(15,'contenttypes','contenttype'),(20,'database','constance'),(17,'registration','registrationprofile'),(18,'registration','supervisedregistrationprofile'),(16,'sessions','session'),(23,'sites','site'),(26,'socialaccount','socialaccount'),(27,'socialaccount','socialapp'),(28,'socialaccount','socialtoken');
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
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-10-19 18:44:29.498013'),(2,'auth','0001_initial','2020-09-26 21:58:29.025619'),(3,'admin','0001_initial','2020-09-26 21:58:29.659220'),(4,'admin','0002_logentry_remove_auto_add','2020-09-26 21:58:29.755076'),(5,'admin','0003_logentry_add_action_flag_choices','2020-09-26 21:58:29.768123'),(6,'askapp','0001_initial','2020-09-26 21:58:30.246910'),(7,'askapp','0002_thread_thumbnail','2020-09-26 21:58:30.695898'),(8,'askapp','0003_profile','2020-09-26 21:58:30.750171'),(9,'askapp','0004_auto_20161226_1858','2020-09-26 21:58:31.320132'),(10,'askapp','0005_auto_20161227_1123','2020-09-26 21:58:31.853940'),(11,'askapp','0006_post_deleted','2020-09-26 21:58:32.031575'),(12,'askapp','0007_auto_20161228_0818','2020-09-26 21:58:32.123546'),(13,'askapp','0008_auto_20161228_1931','2020-09-26 21:58:32.395629'),(14,'askapp','0009_auto_20170105_1944','2020-09-26 21:58:32.606420'),(15,'askapp','0010_auto_20170106_0657','2020-09-26 21:58:32.637783'),(16,'askapp','0011_auto_20170110_1905','2020-09-26 21:58:32.888390'),(17,'askapp','0012_auto_20170203_1436','2020-09-26 21:58:33.223488'),(18,'askapp','0013_auto_20170206_0748','2020-09-26 21:58:33.338845'),(19,'askapp','0014_auto_20170529_1106','2020-09-26 21:58:33.474184'),(20,'askapp','0015_thread_domain','2020-09-26 21:58:33.544614'),(21,'askapp','0016_populate_domain','2020-09-26 21:58:33.574611'),(22,'askapp','0017_auto_20191105_1229','2020-09-26 21:58:33.669750'),(23,'askapp','0018_auto_20191109_1248','2020-09-26 21:58:33.765568'),(24,'askapp','0019_auto_20191119_0846','2020-09-26 21:58:33.943705'),(25,'contenttypes','0002_remove_content_type_name','2020-09-26 21:58:34.110056'),(26,'auth','0002_alter_permission_name_max_length','2020-09-26 21:58:34.143061'),(27,'auth','0003_alter_user_email_max_length','2020-09-26 21:58:34.193309'),(28,'auth','0004_alter_user_username_opts','2020-09-26 21:58:34.223287'),(29,'auth','0005_alter_user_last_login_null','2020-09-26 21:58:34.268763'),(30,'auth','0006_require_contenttypes_0002','2020-09-26 21:58:34.271412'),(31,'auth','0007_alter_validators_add_error_messages','2020-09-26 21:58:34.295259'),(32,'auth','0008_alter_user_username_max_length','2020-09-26 21:58:34.374245'),(33,'auth','0009_alter_user_last_name_max_length','2020-09-26 21:58:34.520196'),(34,'auth','0010_alter_group_name_max_length','2020-09-26 21:58:34.561457'),(35,'auth','0011_update_proxy_permissions','2020-09-26 21:58:34.602354'),(36,'registration','0001_initial','2020-09-26 21:58:34.645033'),(37,'registration','0002_registrationprofile_activated','2020-09-26 21:58:34.732076'),(38,'registration','0003_migrate_activatedstatus','2020-09-26 21:58:34.762271'),(39,'registration','0004_supervisedregistrationprofile','2020-09-26 21:58:34.798096'),(40,'sessions','0001_initial','2020-09-26 21:58:34.869995'),(41,'registration','0004_supervisedregistrationprofile','2020-10-19 18:44:35.973952'),(42,'database','0001_initial','2020-10-18 18:43:51.918819'),(43,'database','0002_auto_20190129_2304','2020-10-18 18:43:52.102986'),(44,'account','0001_initial','2020-11-04 18:58:00.091068'),(45,'account','0002_email_max_length','2020-11-04 18:58:00.230112'),(46,'askapp','0020_auto_20201101_1818','2020-11-04 18:58:00.450512'),(47,'auth','0012_alter_user_first_name_max_length','2020-11-04 18:58:00.496080'),(48,'sites','0001_initial','2020-11-04 18:58:00.555526'),(49,'sites','0002_alter_domain_unique','2020-11-04 18:58:00.591848'),(50,'socialaccount','0001_initial','2020-11-04 18:58:00.838835'),(51,'socialaccount','0002_token_max_lengths','2020-11-04 18:58:01.131134'),(52,'socialaccount','0003_extra_data_default_dict','2020-11-04 18:58:01.159920');
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
INSERT INTO `django_session` VALUES ('1ypco8z4t2orjdt1xjxp8iikz0d0kg29','MTBmZmJkMjA5ZDAzYWFhYmMyZjJmMzJjMzA3ODQyNWZiOTY4YTQzYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkMDljMWUwZjY2MTQ5NDRmMzhkOTUwYTMyNmI0ZmU3ZDQ3MGVhMWJlIn0=','2020-11-02 19:18:50.363711');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
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

--
-- Table structure for table `socialaccount_socialaccount`
--

DROP TABLE IF EXISTS `socialaccount_socialaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialaccount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `uid` varchar(191) NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  KEY `socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id` (`user_id`),
  CONSTRAINT `socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialaccount`
--

LOCK TABLES `socialaccount_socialaccount` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialaccount` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp`
--

DROP TABLE IF EXISTS `socialaccount_socialapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialapp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `name` varchar(40) NOT NULL,
  `client_id` varchar(191) NOT NULL,
  `secret` varchar(191) NOT NULL,
  `key` varchar(191) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp`
--

LOCK TABLES `socialaccount_socialapp` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp_sites`
--

DROP TABLE IF EXISTS `socialaccount_socialapp_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialapp_sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `socialapp_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialapp_sites_socialapp_id_site_id_71a9a768_uniq` (`socialapp_id`,`site_id`),
  KEY `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` (`site_id`),
  CONSTRAINT `socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc` FOREIGN KEY (`socialapp_id`) REFERENCES `socialaccount_socialapp` (`id`),
  CONSTRAINT `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp_sites`
--

LOCK TABLES `socialaccount_socialapp_sites` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialtoken`
--

DROP TABLE IF EXISTS `socialaccount_socialtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialtoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `token_secret` longtext NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int(11) NOT NULL,
  `app_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  KEY `socialaccount_social_account_id_951f210e_fk_socialacc` (`account_id`),
  CONSTRAINT `socialaccount_social_account_id_951f210e_fk_socialacc` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  CONSTRAINT `socialaccount_social_app_id_636a42d7_fk_socialacc` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialtoken`
--

LOCK TABLES `socialaccount_socialtoken` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialtoken` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-04 19:02:35
