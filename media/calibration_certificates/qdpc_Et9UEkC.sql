-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 02, 2024 at 01:49 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `qdpc`
--

-- --------------------------------------------------------

--
-- Table structure for table `authtoken_token`
--

CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add user', 6, 'add_user'),
(22, 'Can change user', 6, 'change_user'),
(23, 'Can delete user', 6, 'delete_user'),
(24, 'Can view user', 6, 'view_user'),
(25, 'Can add acceptance test', 7, 'add_acceptancetest'),
(26, 'Can change acceptance test', 7, 'change_acceptancetest'),
(27, 'Can delete acceptance test', 7, 'delete_acceptancetest'),
(28, 'Can view acceptance test', 7, 'view_acceptancetest'),
(29, 'Can add center', 8, 'add_center'),
(30, 'Can change center', 8, 'change_center'),
(31, 'Can delete center', 8, 'delete_center'),
(32, 'Can view center', 8, 'view_center'),
(33, 'Can add Division', 9, 'add_division'),
(34, 'Can change Division', 9, 'change_division'),
(35, 'Can delete Division', 9, 'delete_division'),
(36, 'Can view Division', 9, 'view_division'),
(37, 'Can add document category', 10, 'add_documentcategory'),
(38, 'Can change document category', 10, 'change_documentcategory'),
(39, 'Can delete document category', 10, 'delete_documentcategory'),
(40, 'Can view document category', 10, 'view_documentcategory'),
(41, 'Can add end use', 11, 'add_enduse'),
(42, 'Can change end use', 11, 'change_enduse'),
(43, 'Can delete end use', 11, 'delete_enduse'),
(44, 'Can view end use', 11, 'view_enduse'),
(45, 'Can add Industry', 12, 'add_goco'),
(46, 'Can change Industry', 12, 'change_goco'),
(47, 'Can delete Industry', 12, 'delete_goco'),
(48, 'Can view Industry', 12, 'view_goco'),
(49, 'Can add Industry', 13, 'add_industry'),
(50, 'Can change Industry', 13, 'change_industry'),
(51, 'Can delete Industry', 13, 'delete_industry'),
(52, 'Can view Industry', 13, 'view_industry'),
(53, 'Can add processing agency', 14, 'add_processingagency'),
(54, 'Can change processing agency', 14, 'change_processingagency'),
(55, 'Can delete processing agency', 14, 'delete_processingagency'),
(56, 'Can view processing agency', 14, 'view_processingagency'),
(57, 'Can add product category', 15, 'add_productcategory'),
(58, 'Can change product category', 15, 'change_productcategory'),
(59, 'Can delete product category', 15, 'delete_productcategory'),
(60, 'Can view product category', 15, 'view_productcategory'),
(61, 'Can add product component', 16, 'add_productcomponent'),
(62, 'Can change product component', 16, 'change_productcomponent'),
(63, 'Can delete product component', 16, 'delete_productcomponent'),
(64, 'Can view product component', 16, 'view_productcomponent'),
(65, 'Can add raw material', 17, 'add_rawmaterial'),
(66, 'Can change raw material', 17, 'change_rawmaterial'),
(67, 'Can delete raw material', 17, 'delete_rawmaterial'),
(68, 'Can view raw material', 17, 'view_rawmaterial'),
(69, 'Can add raw material acceptance test', 18, 'add_rawmaterialacceptancetest'),
(70, 'Can change raw material acceptance test', 18, 'change_rawmaterialacceptancetest'),
(71, 'Can delete raw material acceptance test', 18, 'delete_rawmaterialacceptancetest'),
(72, 'Can view raw material acceptance test', 18, 'view_rawmaterialacceptancetest'),
(73, 'Can add Source', 19, 'add_sources'),
(74, 'Can change Source', 19, 'change_sources'),
(75, 'Can delete Source', 19, 'delete_sources'),
(76, 'Can view Source', 19, 'view_sources'),
(77, 'Can add Supplier', 20, 'add_suppliers'),
(78, 'Can change Supplier', 20, 'change_suppliers'),
(79, 'Can delete Supplier', 20, 'delete_suppliers'),
(80, 'Can view Supplier', 20, 'view_suppliers'),
(81, 'Can add testing agency', 21, 'add_testingagency'),
(82, 'Can change testing agency', 21, 'change_testingagency'),
(83, 'Can delete testing agency', 21, 'delete_testingagency'),
(84, 'Can view testing agency', 21, 'view_testingagency'),
(85, 'Can add unit', 22, 'add_unit'),
(86, 'Can change unit', 22, 'change_unit'),
(87, 'Can delete unit', 22, 'delete_unit'),
(88, 'Can view unit', 22, 'view_unit'),
(89, 'Can add user type', 23, 'add_usertype'),
(90, 'Can change user type', 23, 'change_usertype'),
(91, 'Can delete user type', 23, 'delete_usertype'),
(92, 'Can view user type', 23, 'view_usertype'),
(93, 'Can add role', 24, 'add_role'),
(94, 'Can change role', 24, 'change_role'),
(95, 'Can delete role', 24, 'delete_role'),
(96, 'Can view role', 24, 'view_role'),
(97, 'Can add test result', 25, 'add_testresult'),
(98, 'Can change test result', 25, 'change_testresult'),
(99, 'Can delete test result', 25, 'delete_testresult'),
(100, 'Can view test result', 25, 'view_testresult'),
(101, 'Can add reset password', 26, 'add_resetpassword'),
(102, 'Can change reset password', 26, 'change_resetpassword'),
(103, 'Can delete reset password', 26, 'delete_resetpassword'),
(104, 'Can view reset password', 26, 'view_resetpassword'),
(105, 'Can add raw material document', 27, 'add_rawmaterialdocument'),
(106, 'Can change raw material document', 27, 'change_rawmaterialdocument'),
(107, 'Can delete raw material document', 27, 'delete_rawmaterialdocument'),
(108, 'Can view raw material document', 27, 'view_rawmaterialdocument'),
(109, 'Can add raw material batch', 28, 'add_rawmaterialbatch'),
(110, 'Can change raw material batch', 28, 'change_rawmaterialbatch'),
(111, 'Can delete raw material batch', 28, 'delete_rawmaterialbatch'),
(112, 'Can view raw material batch', 28, 'view_rawmaterialbatch'),
(113, 'Can add product', 29, 'add_product'),
(114, 'Can change product', 29, 'change_product'),
(115, 'Can delete product', 29, 'delete_product'),
(116, 'Can view product', 29, 'view_product'),
(117, 'Can add acceptance test result', 30, 'add_acceptancetestresult'),
(118, 'Can change acceptance test result', 30, 'change_acceptancetestresult'),
(119, 'Can delete acceptance test result', 30, 'delete_acceptancetestresult'),
(120, 'Can view acceptance test result', 30, 'view_acceptancetestresult'),
(121, 'Can add Token', 31, 'add_token'),
(122, 'Can change Token', 31, 'change_token'),
(123, 'Can delete Token', 31, 'delete_token'),
(124, 'Can view Token', 31, 'view_token'),
(125, 'Can add Token', 32, 'add_tokenproxy'),
(126, 'Can change Token', 32, 'change_tokenproxy'),
(127, 'Can delete Token', 32, 'delete_tokenproxy'),
(128, 'Can view Token', 32, 'view_tokenproxy');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(31, 'authtoken', 'token'),
(32, 'authtoken', 'tokenproxy'),
(4, 'contenttypes', 'contenttype'),
(7, 'qdpc_core_models', 'acceptancetest'),
(30, 'qdpc_core_models', 'acceptancetestresult'),
(8, 'qdpc_core_models', 'center'),
(9, 'qdpc_core_models', 'division'),
(10, 'qdpc_core_models', 'documentcategory'),
(11, 'qdpc_core_models', 'enduse'),
(12, 'qdpc_core_models', 'goco'),
(13, 'qdpc_core_models', 'industry'),
(14, 'qdpc_core_models', 'processingagency'),
(29, 'qdpc_core_models', 'product'),
(15, 'qdpc_core_models', 'productcategory'),
(16, 'qdpc_core_models', 'productcomponent'),
(17, 'qdpc_core_models', 'rawmaterial'),
(18, 'qdpc_core_models', 'rawmaterialacceptancetest'),
(28, 'qdpc_core_models', 'rawmaterialbatch'),
(27, 'qdpc_core_models', 'rawmaterialdocument'),
(26, 'qdpc_core_models', 'resetpassword'),
(24, 'qdpc_core_models', 'role'),
(19, 'qdpc_core_models', 'sources'),
(20, 'qdpc_core_models', 'suppliers'),
(21, 'qdpc_core_models', 'testingagency'),
(25, 'qdpc_core_models', 'testresult'),
(22, 'qdpc_core_models', 'unit'),
(6, 'qdpc_core_models', 'user'),
(23, 'qdpc_core_models', 'usertype'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-09-02 11:49:02.754070'),
(2, 'contenttypes', '0002_remove_content_type_name', '2024-09-02 11:49:02.782274'),
(3, 'auth', '0001_initial', '2024-09-02 11:49:02.908429'),
(4, 'auth', '0002_alter_permission_name_max_length', '2024-09-02 11:49:02.939794'),
(5, 'auth', '0003_alter_user_email_max_length', '2024-09-02 11:49:02.943792'),
(6, 'auth', '0004_alter_user_username_opts', '2024-09-02 11:49:02.946793'),
(7, 'auth', '0005_alter_user_last_login_null', '2024-09-02 11:49:02.950802'),
(8, 'auth', '0006_require_contenttypes_0002', '2024-09-02 11:49:02.951802'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2024-09-02 11:49:02.955803'),
(10, 'auth', '0008_alter_user_username_max_length', '2024-09-02 11:49:02.958804'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2024-09-02 11:49:02.962314'),
(12, 'auth', '0010_alter_group_name_max_length', '2024-09-02 11:49:02.968325'),
(13, 'auth', '0011_update_proxy_permissions', '2024-09-02 11:49:02.973325'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2024-09-02 11:49:02.976327'),
(15, 'qdpc_core_models', '0001_initial', '2024-09-02 11:49:04.591603'),
(16, 'admin', '0001_initial', '2024-09-02 11:49:04.668107'),
(17, 'admin', '0002_logentry_remove_auto_add', '2024-09-02 11:49:04.677922'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2024-09-02 11:49:04.687981'),
(19, 'authtoken', '0001_initial', '2024-09-02 11:49:04.771172'),
(20, 'authtoken', '0002_auto_20160226_1747', '2024-09-02 11:49:04.818924'),
(21, 'authtoken', '0003_tokenproxy', '2024-09-02 11:49:04.818924'),
(22, 'authtoken', '0004_alter_tokenproxy_options', '2024-09-02 11:49:04.825753'),
(23, 'sessions', '0001_initial', '2024-09-02 11:49:04.843922');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_acceptancetest`
--

CREATE TABLE `qdpc_core_models_acceptancetest` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `min_value` int(11) NOT NULL,
  `max_value` int(11) NOT NULL,
  `sampling_plan` varchar(100) DEFAULT NULL,
  `reevaluation_frequency_value` int(10) UNSIGNED NOT NULL CHECK (`reevaluation_frequency_value` >= 0),
  `reevaluation_frequency_unit` varchar(10) NOT NULL,
  `unit_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_acceptancetestresult`
--

CREATE TABLE `qdpc_core_models_acceptancetestresult` (
  `id` bigint(20) NOT NULL,
  `test_value` double NOT NULL,
  `test_date` date NOT NULL,
  `validity_date` date DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL,
  `label` varchar(100) DEFAULT NULL,
  `acceptance_test_id` int(11) NOT NULL,
  `raw_material_batch_id` bigint(20) NOT NULL,
  `unit_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_center`
--

CREATE TABLE `qdpc_core_models_center` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `user_type_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_division`
--

CREATE TABLE `qdpc_core_models_division` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `center_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_documentcategory`
--

CREATE TABLE `qdpc_core_models_documentcategory` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_enduse`
--

CREATE TABLE `qdpc_core_models_enduse` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_goco`
--

CREATE TABLE `qdpc_core_models_goco` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `address` varchar(255) NOT NULL,
  `phone_number` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_industry`
--

CREATE TABLE `qdpc_core_models_industry` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `address` varchar(255) NOT NULL,
  `phone_number` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_processingagency`
--

CREATE TABLE `qdpc_core_models_processingagency` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `agency_type` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_product`
--

CREATE TABLE `qdpc_core_models_product` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `specific_use` longtext DEFAULT NULL,
  `shelf_life_value` int(11) DEFAULT NULL,
  `shelf_life_unit` varchar(10) DEFAULT NULL,
  `drawing_number` varchar(100) DEFAULT NULL,
  `drawing_status` varchar(50) DEFAULT NULL,
  `identification_method` varchar(50) NOT NULL,
  `batch_size` longtext DEFAULT NULL,
  `prefix` varchar(50) DEFAULT NULL,
  `suffix` varchar(50) DEFAULT NULL,
  `category_id` int(11) NOT NULL,
  `product_owner_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_productcategory`
--

CREATE TABLE `qdpc_core_models_productcategory` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_productcomponent`
--

CREATE TABLE `qdpc_core_models_productcomponent` (
  `id` bigint(20) NOT NULL,
  `component_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_product_components`
--

CREATE TABLE `qdpc_core_models_product_components` (
  `id` bigint(20) NOT NULL,
  `product_id` bigint(20) NOT NULL,
  `productcomponent_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_product_end_uses`
--

CREATE TABLE `qdpc_core_models_product_end_uses` (
  `id` bigint(20) NOT NULL,
  `product_id` bigint(20) NOT NULL,
  `enduse_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_product_processing_agencies`
--

CREATE TABLE `qdpc_core_models_product_processing_agencies` (
  `id` bigint(20) NOT NULL,
  `product_id` bigint(20) NOT NULL,
  `processingagency_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_product_testing_agencies`
--

CREATE TABLE `qdpc_core_models_product_testing_agencies` (
  `id` bigint(20) NOT NULL,
  `product_id` bigint(20) NOT NULL,
  `testingagency_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_rawmaterial`
--

CREATE TABLE `qdpc_core_models_rawmaterial` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `grade` varchar(50) NOT NULL,
  `shelf_life_value` double NOT NULL,
  `shelf_life_unit` varchar(10) NOT NULL,
  `user_defined_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_rawmaterialacceptancetest`
--

CREATE TABLE `qdpc_core_models_rawmaterialacceptancetest` (
  `id` bigint(20) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `acceptance_test_id` int(11) NOT NULL,
  `created_by_id` bigint(20) DEFAULT NULL,
  `raw_material_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_rawmaterialbatch`
--

CREATE TABLE `qdpc_core_models_rawmaterialbatch` (
  `id` bigint(20) NOT NULL,
  `batch_id` varchar(100) NOT NULL,
  `procurement_date` date NOT NULL,
  `batch_size_value` double NOT NULL,
  `packing_details` longtext NOT NULL,
  `calculate_expiry_date` date DEFAULT NULL,
  `created_on` datetime(6) NOT NULL,
  `acceptence_test_id` bigint(20) NOT NULL,
  `batch_size_unit_id` bigint(20) NOT NULL,
  `created_by_id` bigint(20) DEFAULT NULL,
  `raw_material_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_rawmaterialdocument`
--

CREATE TABLE `qdpc_core_models_rawmaterialdocument` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `issue_no` varchar(255) NOT NULL,
  `revision_no` varchar(255) NOT NULL,
  `release_date` date NOT NULL,
  `approved_by` varchar(255) NOT NULL,
  `document` varchar(100) NOT NULL,
  `validity` int(11) NOT NULL,
  `category_id` bigint(20) NOT NULL,
  `raw_material_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_rawmaterial_acceptance_test`
--

CREATE TABLE `qdpc_core_models_rawmaterial_acceptance_test` (
  `id` bigint(20) NOT NULL,
  `rawmaterial_id` bigint(20) NOT NULL,
  `acceptancetest_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_rawmaterial_sources`
--

CREATE TABLE `qdpc_core_models_rawmaterial_sources` (
  `id` bigint(20) NOT NULL,
  `rawmaterial_id` bigint(20) NOT NULL,
  `sources_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_rawmaterial_suppliers`
--

CREATE TABLE `qdpc_core_models_rawmaterial_suppliers` (
  `id` bigint(20) NOT NULL,
  `rawmaterial_id` bigint(20) NOT NULL,
  `suppliers_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_resetpassword`
--

CREATE TABLE `qdpc_core_models_resetpassword` (
  `id` bigint(20) NOT NULL,
  `reset_key` varchar(50) DEFAULT NULL,
  `used_status` varchar(100) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `updated_on` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_sources`
--

CREATE TABLE `qdpc_core_models_sources` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `address` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_suppliers`
--

CREATE TABLE `qdpc_core_models_suppliers` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `address` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_testingagency`
--

CREATE TABLE `qdpc_core_models_testingagency` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_testresult`
--

CREATE TABLE `qdpc_core_models_testresult` (
  `id` bigint(20) NOT NULL,
  `result_file` varchar(100) NOT NULL,
  `test_date` date NOT NULL,
  `remarks` longtext DEFAULT NULL,
  `acceptance_test_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_unit`
--

CREATE TABLE `qdpc_core_models_unit` (
  `id` bigint(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `abbreviation` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_user`
--

CREATE TABLE `qdpc_core_models_user` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(254) NOT NULL,
  `desired_salutation` varchar(10) NOT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `date_joined` date NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `role_id` varchar(255) DEFAULT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_approved` tinyint(1) NOT NULL,
  `usertype_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_usertype`
--

CREATE TABLE `qdpc_core_models_usertype` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_user_centre`
--

CREATE TABLE `qdpc_core_models_user_centre` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `center_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_user_divisions`
--

CREATE TABLE `qdpc_core_models_user_divisions` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `division_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_user_groups`
--

CREATE TABLE `qdpc_core_models_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_user_role`
--

CREATE TABLE `qdpc_core_models_user_role` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qdpc_core_models_user_user_permissions`
--

CREATE TABLE `qdpc_core_models_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD PRIMARY KEY (`key`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_qdpc_core_models_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `qdpc_core_models_acceptancetest`
--
ALTER TABLE `qdpc_core_models_acceptancetest`
  ADD PRIMARY KEY (`id`),
  ADD KEY `qdpc_core_models_acc_unit_id_6675ca09_fk_qdpc_core` (`unit_id`);

--
-- Indexes for table `qdpc_core_models_acceptancetestresult`
--
ALTER TABLE `qdpc_core_models_acceptancetestresult`
  ADD PRIMARY KEY (`id`),
  ADD KEY `qdpc_core_models_acc_acceptance_test_id_22ada070_fk_qdpc_core` (`acceptance_test_id`),
  ADD KEY `qdpc_core_models_acc_raw_material_batch_i_3a79cae6_fk_qdpc_core` (`raw_material_batch_id`),
  ADD KEY `qdpc_core_models_acc_unit_id_84a4d244_fk_qdpc_core` (`unit_id`);

--
-- Indexes for table `qdpc_core_models_center`
--
ALTER TABLE `qdpc_core_models_center`
  ADD PRIMARY KEY (`id`),
  ADD KEY `qdpc_core_models_cen_user_type_id_c64490ca_fk_qdpc_core` (`user_type_id`);

--
-- Indexes for table `qdpc_core_models_division`
--
ALTER TABLE `qdpc_core_models_division`
  ADD PRIMARY KEY (`id`),
  ADD KEY `qdpc_core_models_div_center_id_7ba38028_fk_qdpc_core` (`center_id`);

--
-- Indexes for table `qdpc_core_models_documentcategory`
--
ALTER TABLE `qdpc_core_models_documentcategory`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `qdpc_core_models_enduse`
--
ALTER TABLE `qdpc_core_models_enduse`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `qdpc_core_models_goco`
--
ALTER TABLE `qdpc_core_models_goco`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `qdpc_core_models_industry`
--
ALTER TABLE `qdpc_core_models_industry`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `qdpc_core_models_processingagency`
--
ALTER TABLE `qdpc_core_models_processingagency`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `qdpc_core_models_product`
--
ALTER TABLE `qdpc_core_models_product`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `qdpc_core_models_pro_category_id_fac9846d_fk_qdpc_core` (`category_id`),
  ADD KEY `qdpc_core_models_pro_product_owner_id_d6ec86b6_fk_qdpc_core` (`product_owner_id`);

--
-- Indexes for table `qdpc_core_models_productcategory`
--
ALTER TABLE `qdpc_core_models_productcategory`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `qdpc_core_models_productcomponent`
--
ALTER TABLE `qdpc_core_models_productcomponent`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `component_name` (`component_name`);

--
-- Indexes for table `qdpc_core_models_product_components`
--
ALTER TABLE `qdpc_core_models_product_components`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `qdpc_core_models_product_product_id_productcompon_07895b8a_uniq` (`product_id`,`productcomponent_id`),
  ADD KEY `qdpc_core_models_pro_productcomponent_id_1e5e72cc_fk_qdpc_core` (`productcomponent_id`);

--
-- Indexes for table `qdpc_core_models_product_end_uses`
--
ALTER TABLE `qdpc_core_models_product_end_uses`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `qdpc_core_models_product_product_id_enduse_id_747d743f_uniq` (`product_id`,`enduse_id`),
  ADD KEY `qdpc_core_models_pro_enduse_id_22280390_fk_qdpc_core` (`enduse_id`);

--
-- Indexes for table `qdpc_core_models_product_processing_agencies`
--
ALTER TABLE `qdpc_core_models_product_processing_agencies`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `qdpc_core_models_product_product_id_processingage_4f139fcb_uniq` (`product_id`,`processingagency_id`),
  ADD KEY `qdpc_core_models_pro_processingagency_id_7982eec2_fk_qdpc_core` (`processingagency_id`);

--
-- Indexes for table `qdpc_core_models_product_testing_agencies`
--
ALTER TABLE `qdpc_core_models_product_testing_agencies`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `qdpc_core_models_product_product_id_testingagency_e0c300ea_uniq` (`product_id`,`testingagency_id`),
  ADD KEY `qdpc_core_models_pro_testingagency_id_e35e3ba0_fk_qdpc_core` (`testingagency_id`);

--
-- Indexes for table `qdpc_core_models_rawmaterial`
--
ALTER TABLE `qdpc_core_models_rawmaterial`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `qdpc_core_models_rawmaterialacceptancetest`
--
ALTER TABLE `qdpc_core_models_rawmaterialacceptancetest`
  ADD PRIMARY KEY (`id`),
  ADD KEY `qdpc_core_models_raw_acceptance_test_id_388eaff2_fk_qdpc_core` (`acceptance_test_id`),
  ADD KEY `qdpc_core_models_raw_created_by_id_410f24e3_fk_qdpc_core` (`created_by_id`),
  ADD KEY `qdpc_core_models_raw_raw_material_id_70d4d8d9_fk_qdpc_core` (`raw_material_id`);

--
-- Indexes for table `qdpc_core_models_rawmaterialbatch`
--
ALTER TABLE `qdpc_core_models_rawmaterialbatch`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `batch_id` (`batch_id`),
  ADD KEY `qdpc_core_models_raw_acceptence_test_id_b741627b_fk_qdpc_core` (`acceptence_test_id`),
  ADD KEY `qdpc_core_models_raw_batch_size_unit_id_dba21dc5_fk_qdpc_core` (`batch_size_unit_id`),
  ADD KEY `qdpc_core_models_raw_created_by_id_abea2297_fk_qdpc_core` (`created_by_id`),
  ADD KEY `qdpc_core_models_raw_raw_material_id_33f1ac5c_fk_qdpc_core` (`raw_material_id`);

--
-- Indexes for table `qdpc_core_models_rawmaterialdocument`
--
ALTER TABLE `qdpc_core_models_rawmaterialdocument`
  ADD PRIMARY KEY (`id`),
  ADD KEY `qdpc_core_models_raw_category_id_57c11f09_fk_qdpc_core` (`category_id`),
  ADD KEY `qdpc_core_models_raw_raw_material_id_a02ac7cf_fk_qdpc_core` (`raw_material_id`);

--
-- Indexes for table `qdpc_core_models_rawmaterial_acceptance_test`
--
ALTER TABLE `qdpc_core_models_rawmaterial_acceptance_test`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `qdpc_core_models_rawmate_rawmaterial_id_acceptanc_f11df84c_uniq` (`rawmaterial_id`,`acceptancetest_id`),
  ADD KEY `qdpc_core_models_raw_acceptancetest_id_b57d0849_fk_qdpc_core` (`acceptancetest_id`);

--
-- Indexes for table `qdpc_core_models_rawmaterial_sources`
--
ALTER TABLE `qdpc_core_models_rawmaterial_sources`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `qdpc_core_models_rawmate_rawmaterial_id_sources_i_f2f03695_uniq` (`rawmaterial_id`,`sources_id`),
  ADD KEY `qdpc_core_models_raw_sources_id_f262cf2f_fk_qdpc_core` (`sources_id`);

--
-- Indexes for table `qdpc_core_models_rawmaterial_suppliers`
--
ALTER TABLE `qdpc_core_models_rawmaterial_suppliers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `qdpc_core_models_rawmate_rawmaterial_id_suppliers_b8caae93_uniq` (`rawmaterial_id`,`suppliers_id`),
  ADD KEY `qdpc_core_models_raw_suppliers_id_ca1d61e7_fk_qdpc_core` (`suppliers_id`);

--
-- Indexes for table `qdpc_core_models_resetpassword`
--
ALTER TABLE `qdpc_core_models_resetpassword`
  ADD PRIMARY KEY (`id`),
  ADD KEY `qdpc_core_models_res_user_id_d1ed9485_fk_qdpc_core` (`user_id`);

--
-- Indexes for table `qdpc_core_models_sources`
--
ALTER TABLE `qdpc_core_models_sources`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `qdpc_core_models_suppliers`
--
ALTER TABLE `qdpc_core_models_suppliers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `qdpc_core_models_testingagency`
--
ALTER TABLE `qdpc_core_models_testingagency`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `qdpc_core_models_testresult`
--
ALTER TABLE `qdpc_core_models_testresult`
  ADD PRIMARY KEY (`id`),
  ADD KEY `qdpc_core_models_tes_acceptance_test_id_3bb1adb4_fk_qdpc_core` (`acceptance_test_id`);

--
-- Indexes for table `qdpc_core_models_unit`
--
ALTER TABLE `qdpc_core_models_unit`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `qdpc_core_models_user`
--
ALTER TABLE `qdpc_core_models_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `qdpc_core_models_use_usertype_id_11d5d30c_fk_qdpc_core` (`usertype_id`);

--
-- Indexes for table `qdpc_core_models_usertype`
--
ALTER TABLE `qdpc_core_models_usertype`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `qdpc_core_models_user_centre`
--
ALTER TABLE `qdpc_core_models_user_centre`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `qdpc_core_models_user_centre_user_id_center_id_80553f2b_uniq` (`user_id`,`center_id`),
  ADD KEY `qdpc_core_models_use_center_id_f0f76015_fk_qdpc_core` (`center_id`);

--
-- Indexes for table `qdpc_core_models_user_divisions`
--
ALTER TABLE `qdpc_core_models_user_divisions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `qdpc_core_models_user_di_user_id_division_id_913cec2b_uniq` (`user_id`,`division_id`),
  ADD KEY `qdpc_core_models_use_division_id_4a22ddf7_fk_qdpc_core` (`division_id`);

--
-- Indexes for table `qdpc_core_models_user_groups`
--
ALTER TABLE `qdpc_core_models_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `qdpc_core_models_user_groups_user_id_group_id_338e61c5_uniq` (`user_id`,`group_id`),
  ADD KEY `qdpc_core_models_user_groups_group_id_d72fca99_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `qdpc_core_models_user_role`
--
ALTER TABLE `qdpc_core_models_user_role`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `qdpc_core_models_user_role_user_id_role_id_ff4a85a3_uniq` (`user_id`,`role_id`),
  ADD KEY `qdpc_core_models_user_role_role_id_7ad2c86d_fk_auth_group_id` (`role_id`);

--
-- Indexes for table `qdpc_core_models_user_user_permissions`
--
ALTER TABLE `qdpc_core_models_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `qdpc_core_models_user_us_user_id_permission_id_975ea3fa_uniq` (`user_id`,`permission_id`),
  ADD KEY `qdpc_core_models_use_permission_id_ad9fdbe7_fk_auth_perm` (`permission_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=129;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `qdpc_core_models_acceptancetest`
--
ALTER TABLE `qdpc_core_models_acceptancetest`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_acceptancetestresult`
--
ALTER TABLE `qdpc_core_models_acceptancetestresult`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_center`
--
ALTER TABLE `qdpc_core_models_center`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_division`
--
ALTER TABLE `qdpc_core_models_division`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_documentcategory`
--
ALTER TABLE `qdpc_core_models_documentcategory`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_enduse`
--
ALTER TABLE `qdpc_core_models_enduse`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_goco`
--
ALTER TABLE `qdpc_core_models_goco`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_industry`
--
ALTER TABLE `qdpc_core_models_industry`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_processingagency`
--
ALTER TABLE `qdpc_core_models_processingagency`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_product`
--
ALTER TABLE `qdpc_core_models_product`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_productcategory`
--
ALTER TABLE `qdpc_core_models_productcategory`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_productcomponent`
--
ALTER TABLE `qdpc_core_models_productcomponent`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_product_components`
--
ALTER TABLE `qdpc_core_models_product_components`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_product_end_uses`
--
ALTER TABLE `qdpc_core_models_product_end_uses`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_product_processing_agencies`
--
ALTER TABLE `qdpc_core_models_product_processing_agencies`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_product_testing_agencies`
--
ALTER TABLE `qdpc_core_models_product_testing_agencies`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_rawmaterial`
--
ALTER TABLE `qdpc_core_models_rawmaterial`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_rawmaterialacceptancetest`
--
ALTER TABLE `qdpc_core_models_rawmaterialacceptancetest`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_rawmaterialbatch`
--
ALTER TABLE `qdpc_core_models_rawmaterialbatch`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_rawmaterialdocument`
--
ALTER TABLE `qdpc_core_models_rawmaterialdocument`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_rawmaterial_acceptance_test`
--
ALTER TABLE `qdpc_core_models_rawmaterial_acceptance_test`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_rawmaterial_sources`
--
ALTER TABLE `qdpc_core_models_rawmaterial_sources`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_rawmaterial_suppliers`
--
ALTER TABLE `qdpc_core_models_rawmaterial_suppliers`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_resetpassword`
--
ALTER TABLE `qdpc_core_models_resetpassword`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_sources`
--
ALTER TABLE `qdpc_core_models_sources`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_suppliers`
--
ALTER TABLE `qdpc_core_models_suppliers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_testingagency`
--
ALTER TABLE `qdpc_core_models_testingagency`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_testresult`
--
ALTER TABLE `qdpc_core_models_testresult`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_unit`
--
ALTER TABLE `qdpc_core_models_unit`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_user`
--
ALTER TABLE `qdpc_core_models_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_usertype`
--
ALTER TABLE `qdpc_core_models_usertype`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_user_centre`
--
ALTER TABLE `qdpc_core_models_user_centre`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_user_divisions`
--
ALTER TABLE `qdpc_core_models_user_divisions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_user_groups`
--
ALTER TABLE `qdpc_core_models_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_user_role`
--
ALTER TABLE `qdpc_core_models_user_role`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qdpc_core_models_user_user_permissions`
--
ALTER TABLE `qdpc_core_models_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD CONSTRAINT `authtoken_token_user_id_35299eff_fk_qdpc_core_models_user_id` FOREIGN KEY (`user_id`) REFERENCES `qdpc_core_models_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_qdpc_core_models_user_id` FOREIGN KEY (`user_id`) REFERENCES `qdpc_core_models_user` (`id`);

--
-- Constraints for table `qdpc_core_models_acceptancetest`
--
ALTER TABLE `qdpc_core_models_acceptancetest`
  ADD CONSTRAINT `qdpc_core_models_acc_unit_id_6675ca09_fk_qdpc_core` FOREIGN KEY (`unit_id`) REFERENCES `qdpc_core_models_unit` (`id`);

--
-- Constraints for table `qdpc_core_models_acceptancetestresult`
--
ALTER TABLE `qdpc_core_models_acceptancetestresult`
  ADD CONSTRAINT `qdpc_core_models_acc_acceptance_test_id_22ada070_fk_qdpc_core` FOREIGN KEY (`acceptance_test_id`) REFERENCES `qdpc_core_models_acceptancetest` (`id`),
  ADD CONSTRAINT `qdpc_core_models_acc_raw_material_batch_i_3a79cae6_fk_qdpc_core` FOREIGN KEY (`raw_material_batch_id`) REFERENCES `qdpc_core_models_rawmaterialbatch` (`id`),
  ADD CONSTRAINT `qdpc_core_models_acc_unit_id_84a4d244_fk_qdpc_core` FOREIGN KEY (`unit_id`) REFERENCES `qdpc_core_models_unit` (`id`);

--
-- Constraints for table `qdpc_core_models_center`
--
ALTER TABLE `qdpc_core_models_center`
  ADD CONSTRAINT `qdpc_core_models_cen_user_type_id_c64490ca_fk_qdpc_core` FOREIGN KEY (`user_type_id`) REFERENCES `qdpc_core_models_usertype` (`id`);

--
-- Constraints for table `qdpc_core_models_division`
--
ALTER TABLE `qdpc_core_models_division`
  ADD CONSTRAINT `qdpc_core_models_div_center_id_7ba38028_fk_qdpc_core` FOREIGN KEY (`center_id`) REFERENCES `qdpc_core_models_center` (`id`);

--
-- Constraints for table `qdpc_core_models_product`
--
ALTER TABLE `qdpc_core_models_product`
  ADD CONSTRAINT `qdpc_core_models_pro_category_id_fac9846d_fk_qdpc_core` FOREIGN KEY (`category_id`) REFERENCES `qdpc_core_models_productcategory` (`id`),
  ADD CONSTRAINT `qdpc_core_models_pro_product_owner_id_d6ec86b6_fk_qdpc_core` FOREIGN KEY (`product_owner_id`) REFERENCES `qdpc_core_models_division` (`id`);

--
-- Constraints for table `qdpc_core_models_product_components`
--
ALTER TABLE `qdpc_core_models_product_components`
  ADD CONSTRAINT `qdpc_core_models_pro_product_id_8aa129c0_fk_qdpc_core` FOREIGN KEY (`product_id`) REFERENCES `qdpc_core_models_product` (`id`),
  ADD CONSTRAINT `qdpc_core_models_pro_productcomponent_id_1e5e72cc_fk_qdpc_core` FOREIGN KEY (`productcomponent_id`) REFERENCES `qdpc_core_models_productcomponent` (`id`);

--
-- Constraints for table `qdpc_core_models_product_end_uses`
--
ALTER TABLE `qdpc_core_models_product_end_uses`
  ADD CONSTRAINT `qdpc_core_models_pro_enduse_id_22280390_fk_qdpc_core` FOREIGN KEY (`enduse_id`) REFERENCES `qdpc_core_models_enduse` (`id`),
  ADD CONSTRAINT `qdpc_core_models_pro_product_id_c1916913_fk_qdpc_core` FOREIGN KEY (`product_id`) REFERENCES `qdpc_core_models_product` (`id`);

--
-- Constraints for table `qdpc_core_models_product_processing_agencies`
--
ALTER TABLE `qdpc_core_models_product_processing_agencies`
  ADD CONSTRAINT `qdpc_core_models_pro_processingagency_id_7982eec2_fk_qdpc_core` FOREIGN KEY (`processingagency_id`) REFERENCES `qdpc_core_models_processingagency` (`id`),
  ADD CONSTRAINT `qdpc_core_models_pro_product_id_fd3942a2_fk_qdpc_core` FOREIGN KEY (`product_id`) REFERENCES `qdpc_core_models_product` (`id`);

--
-- Constraints for table `qdpc_core_models_product_testing_agencies`
--
ALTER TABLE `qdpc_core_models_product_testing_agencies`
  ADD CONSTRAINT `qdpc_core_models_pro_product_id_54cbaef0_fk_qdpc_core` FOREIGN KEY (`product_id`) REFERENCES `qdpc_core_models_product` (`id`),
  ADD CONSTRAINT `qdpc_core_models_pro_testingagency_id_e35e3ba0_fk_qdpc_core` FOREIGN KEY (`testingagency_id`) REFERENCES `qdpc_core_models_testingagency` (`id`);

--
-- Constraints for table `qdpc_core_models_rawmaterialacceptancetest`
--
ALTER TABLE `qdpc_core_models_rawmaterialacceptancetest`
  ADD CONSTRAINT `qdpc_core_models_raw_acceptance_test_id_388eaff2_fk_qdpc_core` FOREIGN KEY (`acceptance_test_id`) REFERENCES `qdpc_core_models_acceptancetest` (`id`),
  ADD CONSTRAINT `qdpc_core_models_raw_created_by_id_410f24e3_fk_qdpc_core` FOREIGN KEY (`created_by_id`) REFERENCES `qdpc_core_models_user` (`id`),
  ADD CONSTRAINT `qdpc_core_models_raw_raw_material_id_70d4d8d9_fk_qdpc_core` FOREIGN KEY (`raw_material_id`) REFERENCES `qdpc_core_models_rawmaterial` (`id`);

--
-- Constraints for table `qdpc_core_models_rawmaterialbatch`
--
ALTER TABLE `qdpc_core_models_rawmaterialbatch`
  ADD CONSTRAINT `qdpc_core_models_raw_acceptence_test_id_b741627b_fk_qdpc_core` FOREIGN KEY (`acceptence_test_id`) REFERENCES `qdpc_core_models_rawmaterialacceptancetest` (`id`),
  ADD CONSTRAINT `qdpc_core_models_raw_batch_size_unit_id_dba21dc5_fk_qdpc_core` FOREIGN KEY (`batch_size_unit_id`) REFERENCES `qdpc_core_models_unit` (`id`),
  ADD CONSTRAINT `qdpc_core_models_raw_created_by_id_abea2297_fk_qdpc_core` FOREIGN KEY (`created_by_id`) REFERENCES `qdpc_core_models_user` (`id`),
  ADD CONSTRAINT `qdpc_core_models_raw_raw_material_id_33f1ac5c_fk_qdpc_core` FOREIGN KEY (`raw_material_id`) REFERENCES `qdpc_core_models_rawmaterial` (`id`);

--
-- Constraints for table `qdpc_core_models_rawmaterialdocument`
--
ALTER TABLE `qdpc_core_models_rawmaterialdocument`
  ADD CONSTRAINT `qdpc_core_models_raw_category_id_57c11f09_fk_qdpc_core` FOREIGN KEY (`category_id`) REFERENCES `qdpc_core_models_documentcategory` (`id`),
  ADD CONSTRAINT `qdpc_core_models_raw_raw_material_id_a02ac7cf_fk_qdpc_core` FOREIGN KEY (`raw_material_id`) REFERENCES `qdpc_core_models_rawmaterial` (`id`);

--
-- Constraints for table `qdpc_core_models_rawmaterial_acceptance_test`
--
ALTER TABLE `qdpc_core_models_rawmaterial_acceptance_test`
  ADD CONSTRAINT `qdpc_core_models_raw_acceptancetest_id_b57d0849_fk_qdpc_core` FOREIGN KEY (`acceptancetest_id`) REFERENCES `qdpc_core_models_acceptancetest` (`id`),
  ADD CONSTRAINT `qdpc_core_models_raw_rawmaterial_id_95b9f138_fk_qdpc_core` FOREIGN KEY (`rawmaterial_id`) REFERENCES `qdpc_core_models_rawmaterial` (`id`);

--
-- Constraints for table `qdpc_core_models_rawmaterial_sources`
--
ALTER TABLE `qdpc_core_models_rawmaterial_sources`
  ADD CONSTRAINT `qdpc_core_models_raw_rawmaterial_id_29bcf7fc_fk_qdpc_core` FOREIGN KEY (`rawmaterial_id`) REFERENCES `qdpc_core_models_rawmaterial` (`id`),
  ADD CONSTRAINT `qdpc_core_models_raw_sources_id_f262cf2f_fk_qdpc_core` FOREIGN KEY (`sources_id`) REFERENCES `qdpc_core_models_sources` (`id`);

--
-- Constraints for table `qdpc_core_models_rawmaterial_suppliers`
--
ALTER TABLE `qdpc_core_models_rawmaterial_suppliers`
  ADD CONSTRAINT `qdpc_core_models_raw_rawmaterial_id_b34b330f_fk_qdpc_core` FOREIGN KEY (`rawmaterial_id`) REFERENCES `qdpc_core_models_rawmaterial` (`id`),
  ADD CONSTRAINT `qdpc_core_models_raw_suppliers_id_ca1d61e7_fk_qdpc_core` FOREIGN KEY (`suppliers_id`) REFERENCES `qdpc_core_models_suppliers` (`id`);

--
-- Constraints for table `qdpc_core_models_resetpassword`
--
ALTER TABLE `qdpc_core_models_resetpassword`
  ADD CONSTRAINT `qdpc_core_models_res_user_id_d1ed9485_fk_qdpc_core` FOREIGN KEY (`user_id`) REFERENCES `qdpc_core_models_user` (`id`);

--
-- Constraints for table `qdpc_core_models_testresult`
--
ALTER TABLE `qdpc_core_models_testresult`
  ADD CONSTRAINT `qdpc_core_models_tes_acceptance_test_id_3bb1adb4_fk_qdpc_core` FOREIGN KEY (`acceptance_test_id`) REFERENCES `qdpc_core_models_acceptancetest` (`id`);

--
-- Constraints for table `qdpc_core_models_user`
--
ALTER TABLE `qdpc_core_models_user`
  ADD CONSTRAINT `qdpc_core_models_use_usertype_id_11d5d30c_fk_qdpc_core` FOREIGN KEY (`usertype_id`) REFERENCES `qdpc_core_models_usertype` (`id`);

--
-- Constraints for table `qdpc_core_models_user_centre`
--
ALTER TABLE `qdpc_core_models_user_centre`
  ADD CONSTRAINT `qdpc_core_models_use_center_id_f0f76015_fk_qdpc_core` FOREIGN KEY (`center_id`) REFERENCES `qdpc_core_models_center` (`id`),
  ADD CONSTRAINT `qdpc_core_models_use_user_id_4692322d_fk_qdpc_core` FOREIGN KEY (`user_id`) REFERENCES `qdpc_core_models_user` (`id`);

--
-- Constraints for table `qdpc_core_models_user_divisions`
--
ALTER TABLE `qdpc_core_models_user_divisions`
  ADD CONSTRAINT `qdpc_core_models_use_division_id_4a22ddf7_fk_qdpc_core` FOREIGN KEY (`division_id`) REFERENCES `qdpc_core_models_division` (`id`),
  ADD CONSTRAINT `qdpc_core_models_use_user_id_f1ded676_fk_qdpc_core` FOREIGN KEY (`user_id`) REFERENCES `qdpc_core_models_user` (`id`);

--
-- Constraints for table `qdpc_core_models_user_groups`
--
ALTER TABLE `qdpc_core_models_user_groups`
  ADD CONSTRAINT `qdpc_core_models_use_user_id_f689a04d_fk_qdpc_core` FOREIGN KEY (`user_id`) REFERENCES `qdpc_core_models_user` (`id`),
  ADD CONSTRAINT `qdpc_core_models_user_groups_group_id_d72fca99_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `qdpc_core_models_user_role`
--
ALTER TABLE `qdpc_core_models_user_role`
  ADD CONSTRAINT `qdpc_core_models_use_user_id_c65ec01c_fk_qdpc_core` FOREIGN KEY (`user_id`) REFERENCES `qdpc_core_models_user` (`id`),
  ADD CONSTRAINT `qdpc_core_models_user_role_role_id_7ad2c86d_fk_auth_group_id` FOREIGN KEY (`role_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `qdpc_core_models_user_user_permissions`
--
ALTER TABLE `qdpc_core_models_user_user_permissions`
  ADD CONSTRAINT `qdpc_core_models_use_permission_id_ad9fdbe7_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `qdpc_core_models_use_user_id_a4d8da82_fk_qdpc_core` FOREIGN KEY (`user_id`) REFERENCES `qdpc_core_models_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
