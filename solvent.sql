/*
SQLyog Community v11.31 (32 bit)
MySQL - 5.5.41-0ubuntu0.14.04.1 : Database - template
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`template` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;

USE `template`;

/*Table structure for table `atoms` */

DROP TABLE IF EXISTS `atoms`;

CREATE TABLE `atoms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(32) NOT NULL,
  `session` varchar(11) NOT NULL,
  `windowstation` varchar(18) NOT NULL,
  `atom` varchar(10) NOT NULL,
  `refcount` int(11) NOT NULL,
  `hindex` int(11) NOT NULL,
  `pinned` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `atomscan` */

DROP TABLE IF EXISTS `atomscan`;

CREATE TABLE `atomscan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(32) NOT NULL,
  `atomofs` varchar(32) NOT NULL,
  `atom` varchar(10) NOT NULL,
  `refs` int(11) NOT NULL,
  `pinned` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `callbacks` */

DROP TABLE IF EXISTS `callbacks`;

CREATE TABLE `callbacks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(36) NOT NULL,
  `callback` varchar(32) NOT NULL,
  `module` varchar(20) NOT NULL,
  `details` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `clipboard` */

DROP TABLE IF EXISTS `clipboard`;

CREATE TABLE `clipboard` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `session` varchar(10) NOT NULL,
  `windowstation` varchar(13) NOT NULL,
  `format` varchar(18) NOT NULL,
  `handle` varchar(10) NOT NULL,
  `object` varchar(10) NOT NULL,
  `data` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `cmdline` */

DROP TABLE IF EXISTS `cmdline`;

CREATE TABLE `cmdline` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `process` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `pid` int(22) DEFAULT NULL,
  `commandline` varchar(1024) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `cmdscan` */

DROP TABLE IF EXISTS `cmdscan`;

CREATE TABLE `cmdscan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `commandprocess` varchar(255) COLLATE utf8_bin NOT NULL,
  `commandhistory` varchar(18) COLLATE utf8_bin NOT NULL,
  `application` varchar(255) COLLATE utf8_bin NOT NULL,
  `flags` varchar(255) COLLATE utf8_bin NOT NULL,
  `commandcount` int(11) NOT NULL,
  `lastadded` int(11) NOT NULL,
  `lastdisplayed` int(11) NOT NULL,
  `firstcommand` int(11) NOT NULL,
  `commandcountmax` int(11) NOT NULL,
  `processhandle` varchar(18) COLLATE utf8_bin NOT NULL,
  `cmd1` varchar(10) COLLATE utf8_bin NOT NULL,
  `cmd2` varchar(10) COLLATE utf8_bin NOT NULL,
  `cmd3` varchar(14) COLLATE utf8_bin NOT NULL,
  `cmd4` text COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `consoles` */

DROP TABLE IF EXISTS `consoles`;

CREATE TABLE `consoles` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `consoles` varchar(1024) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `dlldump` */

DROP TABLE IF EXISTS `dlldump`;

CREATE TABLE `dlldump` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `process` varchar(32) COLLATE utf8_bin NOT NULL,
  `name` varchar(255) COLLATE utf8_bin NOT NULL,
  `modulebase` varchar(32) COLLATE utf8_bin NOT NULL,
  `modulename` varchar(255) COLLATE utf8_bin NOT NULL,
  `result` varchar(255) COLLATE utf8_bin NOT NULL,
  `md5` varchar(32) COLLATE utf8_bin DEFAULT NULL,
  `filename` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `fullfilename` text COLLATE utf8_bin,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1196 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `dlllist` */

DROP TABLE IF EXISTS `dlllist`;

CREATE TABLE `dlllist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `process` varchar(255) COLLATE utf8_bin NOT NULL,
  `pid` int(8) NOT NULL,
  `cmd` text COLLATE utf8_bin NOT NULL,
  `servicepack` varchar(20) COLLATE utf8_bin NOT NULL,
  `base` varchar(18) COLLATE utf8_bin NOT NULL,
  `size` varchar(18) COLLATE utf8_bin NOT NULL,
  `loadcount` varchar(18) COLLATE utf8_bin NOT NULL,
  `dllpath` text COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `driverscan` */

DROP TABLE IF EXISTS `driverscan`;

CREATE TABLE `driverscan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(32) NOT NULL,
  `ptr` int(11) NOT NULL,
  `hnd` int(11) NOT NULL,
  `start` varchar(10) NOT NULL,
  `size` varchar(10) NOT NULL,
  `servicekey` varchar(20) NOT NULL,
  `name` varchar(12) NOT NULL,
  `drivername` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `envars` */

DROP TABLE IF EXISTS `envars`;

CREATE TABLE `envars` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `process` varchar(255) NOT NULL,
  `block` varchar(32) NOT NULL,
  `variable` varchar(255) NOT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `filescan` */

DROP TABLE IF EXISTS `filescan`;

CREATE TABLE `filescan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(32) NOT NULL,
  `ptr` int(11) NOT NULL,
  `hnd` int(11) NOT NULL,
  `access` varchar(6) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `gahti` */

DROP TABLE IF EXISTS `gahti`;

CREATE TABLE `gahti` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `session` int(11) NOT NULL,
  `type` varchar(20) NOT NULL,
  `tag` varchar(8) NOT NULL,
  `fndestroy` varchar(10) NOT NULL,
  `flags` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `gditimers` */

DROP TABLE IF EXISTS `gditimers`;

CREATE TABLE `gditimers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sess` int(11) NOT NULL,
  `handle` varchar(10) NOT NULL,
  `object` varchar(10) NOT NULL,
  `thread` int(11) NOT NULL,
  `process` varchar(20) NOT NULL,
  `nid` varchar(10) NOT NULL,
  `rate` int(11) NOT NULL COMMENT 'rate(ms)',
  `countdown` int(11) NOT NULL COMMENT 'countdown(ms)',
  `func` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `gdt` */

DROP TABLE IF EXISTS `gdt`;

CREATE TABLE `gdt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cpu` int(11) NOT NULL,
  `sel` varchar(10) NOT NULL,
  `base` varchar(10) NOT NULL,
  `limit` varchar(10) NOT NULL,
  `type` varchar(14) NOT NULL,
  `dpl` int(11) NOT NULL,
  `gr` varchar(4) NOT NULL,
  `pr` varchar(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `getservicesids` */

DROP TABLE IF EXISTS `getservicesids`;

CREATE TABLE `getservicesids` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `serviceid` varchar(255) NOT NULL,
  `servicename` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `getsids` */

DROP TABLE IF EXISTS `getsids`;

CREATE TABLE `getsids` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `process` text COLLATE utf8_bin NOT NULL,
  `pid` int(11) NOT NULL,
  `sid` text COLLATE utf8_bin NOT NULL,
  `user` text COLLATE utf8_bin NOT NULL,
  `comment` text COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `handles` */

DROP TABLE IF EXISTS `handles`;

CREATE TABLE `handles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(32) NOT NULL,
  `pid` int(6) NOT NULL,
  `handle` varchar(10) NOT NULL,
  `access` varchar(32) NOT NULL,
  `type` varchar(26) NOT NULL,
  `details` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `hivedump` */

DROP TABLE IF EXISTS `hivedump`;

CREATE TABLE `hivedump` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lastwritten` datetime DEFAULT NULL,
  `key` text COLLATE utf8_bin,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `hivelist` */

DROP TABLE IF EXISTS `hivelist`;

CREATE TABLE `hivelist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `virtual` varchar(32) NOT NULL,
  `physical` varchar(32) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `idt` */

DROP TABLE IF EXISTS `idt`;

CREATE TABLE `idt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cpu` int(11) NOT NULL,
  `index` int(11) NOT NULL,
  `selector` varchar(10) NOT NULL,
  `value` varchar(10) NOT NULL,
  `module` varchar(20) NOT NULL,
  `section` varchar(12) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `imageinfo` */

DROP TABLE IF EXISTS `imageinfo`;

CREATE TABLE `imageinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `omschrijving` varchar(32) COLLATE utf8_bin DEFAULT NULL,
  `waarde` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `joblinks` */

DROP TABLE IF EXISTS `joblinks`;

CREATE TABLE `joblinks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(18) NOT NULL,
  `name` varchar(255) NOT NULL,
  `pid` int(11) NOT NULL,
  `ppid` int(11) NOT NULL,
  `sess` int(11) NOT NULL,
  `jobsess` varchar(6) NOT NULL,
  `wow64` varchar(6) NOT NULL,
  `total` varchar(6) NOT NULL,
  `active` varchar(6) NOT NULL,
  `term` varchar(6) NOT NULL,
  `joblink` varchar(8) NOT NULL,
  `process` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `kdbgscan` */

DROP TABLE IF EXISTS `kdbgscan`;

CREATE TABLE `kdbgscan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kdbg` text COLLATE utf8_bin,
  `offsetv` varchar(22) COLLATE utf8_bin DEFAULT NULL,
  `offsetp` varchar(22) COLLATE utf8_bin DEFAULT NULL,
  `kdbgowner` text COLLATE utf8_bin,
  `kdbgheader` text COLLATE utf8_bin,
  `version64` text COLLATE utf8_bin,
  `sp` int(11) DEFAULT NULL,
  `build` text COLLATE utf8_bin,
  `ActiveProcessoffset` varchar(22) COLLATE utf8_bin DEFAULT NULL,
  `ActiveProcess` text COLLATE utf8_bin,
  `LoadedModuleListoffset` varchar(22) COLLATE utf8_bin DEFAULT NULL,
  `LoadedModuleList` text COLLATE utf8_bin,
  `KernelBase` text COLLATE utf8_bin,
  `major` int(11) DEFAULT NULL,
  `minor` int(11) DEFAULT NULL,
  `kpcr` text COLLATE utf8_bin,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `ldrmodules` */

DROP TABLE IF EXISTS `ldrmodules`;

CREATE TABLE `ldrmodules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `process` varchar(255) NOT NULL,
  `base` varchar(18) NOT NULL,
  `inload` varchar(5) NOT NULL,
  `ininit` varchar(5) NOT NULL,
  `inmem` varchar(5) NOT NULL,
  `mappedpath` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `memmap` */

DROP TABLE IF EXISTS `memmap`;

CREATE TABLE `memmap` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `virtual` varchar(18) NOT NULL,
  `physical` varchar(18) NOT NULL,
  `size` varchar(18) NOT NULL,
  `dumpfileoffset` varchar(18) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `memtimeliner` */

DROP TABLE IF EXISTS `memtimeliner`;

CREATE TABLE `memtimeliner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(25) NOT NULL,
  `size` int(22) NOT NULL,
  `type` varchar(4) NOT NULL,
  `mode` varchar(15) NOT NULL,
  `uid` int(11) NOT NULL,
  `gid` int(11) NOT NULL,
  `meta` varchar(25) NOT NULL,
  `filename` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `mftparser` */

DROP TABLE IF EXISTS `mftparser`;

CREATE TABLE `mftparser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(32) COLLATE utf8_bin DEFAULT NULL,
  `attribute` varchar(56) COLLATE utf8_bin DEFAULT NULL,
  `record` int(32) DEFAULT NULL,
  `linkcount` int(11) DEFAULT NULL,
  `standardinformation_creation` datetime DEFAULT NULL,
  `standardinformation_modified` datetime DEFAULT NULL,
  `standardinformation_mft_altered` datetime DEFAULT NULL,
  `standardinformation_accessdate` datetime DEFAULT NULL,
  `standardinformation_type` varchar(256) COLLATE utf8_bin DEFAULT NULL,
  `filename_creation` datetime DEFAULT NULL,
  `filename_modified` datetime DEFAULT NULL,
  `filename_mft_altered` datetime DEFAULT NULL,
  `filename_accessdate` datetime DEFAULT NULL,
  `filename_name_path` varchar(1024) COLLATE utf8_bin DEFAULT NULL,
  `data` blob,
  `object_id` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `birth_volumeid` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `birth_objectid` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `birth_domainid` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `modscan` */

DROP TABLE IF EXISTS `modscan`;

CREATE TABLE `modscan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(18) NOT NULL,
  `name` varchar(255) NOT NULL,
  `base` varchar(18) NOT NULL,
  `size` varchar(18) NOT NULL,
  `file` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `modules` */

DROP TABLE IF EXISTS `modules`;

CREATE TABLE `modules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(18) NOT NULL,
  `name` varchar(255) NOT NULL,
  `base` varchar(18) NOT NULL,
  `size` varchar(18) NOT NULL,
  `file` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `mutantscan` */

DROP TABLE IF EXISTS `mutantscan`;

CREATE TABLE `mutantscan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(18) NOT NULL,
  `ptr` int(11) NOT NULL,
  `hnd` int(11) NOT NULL,
  `signal` int(11) NOT NULL,
  `thread` varchar(18) NOT NULL,
  `cid` varchar(32) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `objtypescan` */

DROP TABLE IF EXISTS `objtypescan`;

CREATE TABLE `objtypescan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(18) NOT NULL,
  `nobjects` varchar(10) NOT NULL,
  `nhandles` varchar(10) NOT NULL,
  `key` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `pooltype` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `plugins` */

DROP TABLE IF EXISTS `plugins`;

CREATE TABLE `plugins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `status` int(11) DEFAULT '0' COMMENT '0 = Not executed. 1 = Executed. 2 = Executing.',
  `started` datetime DEFAULT NULL,
  `stopped` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `preferences` */

DROP TABLE IF EXISTS `preferences`;

CREATE TABLE `preferences` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `plugin` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `row_id` int(11) DEFAULT NULL,
  `action` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `prefetchparser` */

DROP TABLE IF EXISTS `prefetchparser`;

CREATE TABLE `prefetchparser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prefetchfile` varchar(255) NOT NULL,
  `executiontime` datetime NOT NULL,
  `times` int(11) NOT NULL,
  `size` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `printkey` */

DROP TABLE IF EXISTS `printkey`;

CREATE TABLE `printkey` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `register` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `keyname` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `keylegend` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  `lastupdated` datetime DEFAULT NULL,
  `subkeys` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `type` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `values` text COLLATE utf8_bin,
  `legend` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `model` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `privs` */

DROP TABLE IF EXISTS `privs`;

CREATE TABLE `privs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `process` varchar(255) NOT NULL,
  `value` int(11) NOT NULL,
  `privilege` varchar(255) NOT NULL,
  `attributes` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `procdump` */

DROP TABLE IF EXISTS `procdump`;

CREATE TABLE `procdump` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `process` varchar(32) COLLATE utf8_bin DEFAULT NULL,
  `imagebase` varchar(32) COLLATE utf8_bin DEFAULT NULL,
  `name` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `result` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `md5` varchar(32) COLLATE utf8_bin DEFAULT NULL,
  `filename` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `fullfilename` text COLLATE utf8_bin,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `pslist` */

DROP TABLE IF EXISTS `pslist`;

CREATE TABLE `pslist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(32) NOT NULL,
  `name` varchar(20) NOT NULL,
  `pid` int(11) NOT NULL,
  `ppid` int(11) NOT NULL,
  `thds` int(11) NOT NULL,
  `hnds` int(11) NOT NULL,
  `sess` int(11) NOT NULL,
  `wow64` int(11) NOT NULL,
  `start` datetime NOT NULL,
  `exit` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `psscan` */

DROP TABLE IF EXISTS `psscan`;

CREATE TABLE `psscan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(18) NOT NULL,
  `name` varchar(255) NOT NULL,
  `pid` int(11) NOT NULL,
  `ppid` int(11) NOT NULL,
  `pdb` varchar(18) NOT NULL,
  `timecreated` datetime NOT NULL,
  `timeexited` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `pstree` */

DROP TABLE IF EXISTS `pstree`;

CREATE TABLE `pstree` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `depth` int(11) DEFAULT NULL,
  `offset` varchar(20) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `pid` int(11) NOT NULL,
  `ppid` int(11) NOT NULL,
  `thds` int(11) NOT NULL,
  `hnds` int(11) NOT NULL,
  `plugin_time` datetime NOT NULL,
  `audit` text,
  `cmd` text,
  `path` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `psxview` */

DROP TABLE IF EXISTS `psxview`;

CREATE TABLE `psxview` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(10) NOT NULL,
  `name` varchar(20) NOT NULL,
  `pid` int(11) NOT NULL,
  `pslist` varchar(6) NOT NULL,
  `psscan` varchar(6) NOT NULL,
  `thrdproc` varchar(8) NOT NULL,
  `pspcid` varchar(6) NOT NULL,
  `csrss` varchar(5) NOT NULL,
  `session` varchar(7) NOT NULL,
  `deskthrd` varchar(8) NOT NULL,
  `exittime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `settings` */

DROP TABLE IF EXISTS `settings`;

CREATE TABLE `settings` (
  `md5hash` varchar(32) COLLATE utf8_bin NOT NULL,
  `initialized` datetime NOT NULL,
  `filename` varchar(255) COLLATE utf8_bin NOT NULL,
  `directory` varchar(255) COLLATE utf8_bin NOT NULL,
  `filepath` varchar(255) COLLATE utf8_bin NOT NULL,
  `caseid` int(11) NOT NULL,
  `profile` varchar(255) COLLATE utf8_bin NOT NULL,
  `description` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `shimcache` */

DROP TABLE IF EXISTS `shimcache`;

CREATE TABLE `shimcache` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lastmodified` datetime NOT NULL,
  `lastupdate` datetime NOT NULL,
  `path` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `sockets` */

DROP TABLE IF EXISTS `sockets`;

CREATE TABLE `sockets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `memtype` varchar(12) DEFAULT NULL,
  `offset` varchar(18) NOT NULL,
  `pid` int(11) NOT NULL,
  `port` int(11) NOT NULL,
  `proto` int(11) NOT NULL,
  `protocol` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `createtime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;

/*Table structure for table `sockscan` */

DROP TABLE IF EXISTS `sockscan`;

CREATE TABLE `sockscan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(18) NOT NULL,
  `pid` int(11) NOT NULL,
  `port` int(11) NOT NULL,
  `proto` int(11) NOT NULL,
  `protocol` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `createtime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `ssdt` */

DROP TABLE IF EXISTS `ssdt`;

CREATE TABLE `ssdt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ssdt` varchar(11) COLLATE utf8_bin NOT NULL,
  `mem1` varchar(18) COLLATE utf8_bin NOT NULL,
  `entry` varchar(18) COLLATE utf8_bin NOT NULL,
  `mem2` varchar(18) COLLATE utf8_bin NOT NULL,
  `systemcall` varchar(255) COLLATE utf8_bin NOT NULL,
  `owner` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `strings` */

DROP TABLE IF EXISTS `strings`;

CREATE TABLE `strings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(22) COLLATE utf8_bin DEFAULT NULL,
  `string` text COLLATE utf8_bin,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `symlinkscan` */

DROP TABLE IF EXISTS `symlinkscan`;

CREATE TABLE `symlinkscan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(18) NOT NULL,
  `ptr` int(11) NOT NULL,
  `hnd` int(11) NOT NULL,
  `creationtime` datetime NOT NULL,
  `from` varchar(255) NOT NULL,
  `to` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `thrdscan` */

DROP TABLE IF EXISTS `thrdscan`;

CREATE TABLE `thrdscan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(18) NOT NULL,
  `pid` int(11) NOT NULL,
  `tid` int(11) NOT NULL,
  `startaddress` varchar(18) NOT NULL,
  `createtime` datetime NOT NULL,
  `exittime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `timers` */

DROP TABLE IF EXISTS `timers`;

CREATE TABLE `timers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offset` varchar(10) NOT NULL,
  `duetime` varchar(32) NOT NULL,
  `period` int(11) NOT NULL COMMENT 'in ms',
  `signaled` varchar(3) NOT NULL,
  `routine` varchar(10) NOT NULL,
  `module` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `unloadedmodules` */

DROP TABLE IF EXISTS `unloadedmodules`;

CREATE TABLE `unloadedmodules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `startaddress` varchar(12) NOT NULL,
  `endaddress` varchar(12) NOT NULL,
  `plugin_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `userhandles` */

DROP TABLE IF EXISTS `userhandles`;

CREATE TABLE `userhandles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sharedinfo` varchar(10) NOT NULL,
  `sessionid` int(11) NOT NULL,
  `shareddelta` int(11) NOT NULL,
  `ahelist` varchar(10) NOT NULL,
  `tablesize` varchar(10) NOT NULL,
  `entrysize` varchar(10) NOT NULL,
  `object` varchar(10) NOT NULL,
  `handle` varchar(10) NOT NULL,
  `btype` varchar(20) NOT NULL,
  `flags` int(11) NOT NULL,
  `thread` varchar(8) NOT NULL,
  `process` varchar(8) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `vadwalk` */

DROP TABLE IF EXISTS `vadwalk`;

CREATE TABLE `vadwalk` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `address` varchar(10) NOT NULL,
  `parent` varchar(10) NOT NULL,
  `left` varchar(10) NOT NULL,
  `right` varchar(10) NOT NULL,
  `start` varchar(10) NOT NULL,
  `end` varchar(10) NOT NULL,
  `tag` varchar(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
