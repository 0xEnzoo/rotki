import {
  RiAccountCircleLine,
  RiAddBoxLine,
  RiAddCircleLine,
  RiAddLine,
  RiAdminLine,
  RiAlarmWarningLine,
  RiArchiveStackAddLine,
  RiArchiveStackReduceLine,
  RiArrowDownCircleLine,
  RiArrowDownLine,
  RiArrowDownSLine,
  RiArrowGoBackLine,
  RiArrowGoForwardLine,
  RiArrowLeftLine,
  RiArrowLeftRightLine,
  RiArrowRightLine,
  RiArrowRightSLine,
  RiArrowUpCircleLine,
  RiArrowUpDownLine,
  RiArrowUpLine,
  RiArrowUpSLine,
  RiBankLine,
  RiBarChartBoxLine,
  RiBook2Line,
  RiBookOpenLine,
  RiBookReadLine,
  RiBox3Line,
  RiBriefcaseLine,
  RiBugLine,
  RiCalculatorLine,
  RiCalendar2Line,
  RiCalendarEventLine,
  RiCalendarLine,
  RiCashLine,
  RiChatQuoteLine,
  RiCheckDoubleLine,
  RiCheckboxCircleLine,
  RiCheckboxIndeterminateLine,
  RiCheckboxMultipleLine,
  RiCloseLine,
  RiCloudLine,
  RiCloudOffLine,
  RiCodeBoxLine,
  RiCoinLine,
  RiCoinsLine,
  RiContactsLine,
  RiContrastDropFill,
  RiCopyrightLine,
  RiCornerLeftUpLine,
  RiDashboardLine,
  RiDatabase2Line,
  RiDatabaseLine,
  RiDeleteBin5Line,
  RiDeleteBinFill,
  RiDeleteBinLine,
  RiDiscordLine,
  RiDownloadCloud2Line,
  RiDownloadCloudLine,
  RiDownloadLine,
  RiDropFill,
  RiEarthLine,
  RiEditLine,
  RiEqualLine,
  RiEqualizerLine,
  RiErrorWarningLine,
  RiExchangeBoxLine,
  RiExchangeLine,
  RiExternalLinkLine,
  RiEye2Line,
  RiEyeLine,
  RiEyeOffLine,
  RiFileAddLine,
  RiFileChartLine,
  RiFileCloseLine,
  RiFileCopyLine,
  RiFileDownloadLine,
  RiFileEditLine,
  RiFileInfoLine,
  RiFileList3Line,
  RiFileSearchLine,
  RiFileSettingsLine,
  RiFileTextLine,
  RiFileUploadLine,
  RiFilterLine,
  RiFireLine,
  RiFolderLine,
  RiFolderOpenLine,
  RiFolderReceivedLine,
  RiFolderReduceLine,
  RiGift2Line,
  RiGiftLine,
  RiGitBranchLine,
  RiGitCommitLine,
  RiGitMergeLine,
  RiGithubLine,
  RiGovernmentLine,
  RiHandCoinLine,
  RiHandHeartLine,
  RiHeart2Line,
  RiHistoryLine,
  RiHome3Line,
  RiImageLine,
  RiInboxArchiveLine,
  RiInformationLine,
  RiKeyLine,
  RiLayoutGridLine,
  RiLeafLine,
  RiLineChartLine,
  RiLink,
  RiLinksLine,
  RiListCheck2,
  RiListRadio,
  RiListUnordered,
  RiLock2Fill,
  RiLockLine,
  RiLockUnlockLine,
  RiLoginCircleLine,
  RiLogoutBoxRLine,
  RiLogoutCircleRLine,
  RiLoopLeftLine,
  RiLoopRightLine,
  RiMapPinTimeLine,
  RiMedalLine,
  RiMoonLine,
  RiMore2Fill,
  RiNotification3Line,
  RiNotificationLine,
  RiPaletteLine,
  RiPencilLine,
  RiPercentLine,
  RiPlayListAddLine,
  RiPriceTagLine,
  RiPushpinFill,
  RiPushpinLine,
  RiQuestionLine,
  RiQuestionnaireLine,
  RiQuillPenLine,
  RiRefreshLine,
  RiRefund2Line,
  RiRepeat2Line,
  RiRestartLine,
  RiRocket2Line,
  RiRocketLine,
  RiSave2Fill,
  RiSaveLine,
  RiScalesFill,
  RiScalesLine,
  RiScreenshot2Line,
  RiSearchLine,
  RiSeedlingLine,
  RiSendPlane2Line,
  RiServerLine,
  RiSettings2Line,
  RiSettings3Line,
  RiSettings4Line,
  RiShakeHandsLine,
  RiShareCircleLine,
  RiShuffleLine,
  RiSortAsc,
  RiSortDesc,
  RiSparklingLine,
  RiStickyNoteLine,
  RiSubtractLine,
  RiSuitcase2Line,
  RiSunLine,
  RiSwapBoxLine,
  RiSwapLine,
  RiTokenSwapLine,
  RiTrophyLine,
  RiTwitterXLine,
  RiUnpinLine,
  RiUploadCloud2Line,
  RiUploadCloudLine,
  RiUploadLine,
  RiUser2Line,
  RiUserLine,
  RiUserSettingsLine,
  RiVipCrownLine,
  RiVirusLine,
  RiWallet3Line,
  RiWaterPercentLine,
  RiWifiLine,
  RiWifiOffLine,
  type RuiOptions,
  ThemeMode,
  createRui,
} from '@rotki/ui-library-compat';
import '@rotki/ui-library-compat/style.css';

export default (defaults: Partial<RuiOptions['defaults']>) =>
  createRui({
    theme: {
      mode: ThemeMode.light,
      icons: [
        RiDashboardLine,
        RiWallet3Line,
        RiCoinsLine,
        RiExchangeLine,
        RiScalesLine,
        RiScalesFill,
        RiImageLine,
        RiHistoryLine,
        RiShuffleLine,
        RiBankLine,
        RiExchangeBoxLine,
        RiBookReadLine,
        RiLineChartLine,
        RiBarChartBoxLine,
        RiLoginCircleLine,
        RiLogoutCircleRLine,
        RiSearchLine,
        RiArrowRightSLine,
        RiAddCircleLine,
        RiGiftLine,
        RiFileChartLine,
        RiInboxArchiveLine,
        RiCalculatorLine,
        RiDatabase2Line,
        RiServerLine,
        RiDatabaseLine,
        RiListRadio,
        RiCalendarEventLine,
        RiCalendar2Line,
        RiBook2Line,
        RiKeyLine,
        RiVipCrownLine,
        RiSwapLine,
        RiLinksLine,
        RiFolderReceivedLine,
        RiSettings4Line,
        RiArrowUpLine,
        RiArrowDownLine,
        RiScreenshot2Line,
        RiArrowLeftLine,
        RiStickyNoteLine,
        RiNotification3Line,
        RiPencilLine,
        RiQuestionLine,
        RiLogoutBoxRLine,
        RiAccountCircleLine,
        RiEyeLine,
        RiEye2Line,
        RiEyeOffLine,
        RiArrowDownSLine,
        RiMoonLine,
        RiSunLine,
        RiRestartLine,
        RiRefreshLine,
        RiCodeBoxLine,
        RiSave2Fill,
        RiDeleteBinFill,
        RiDeleteBinLine,
        RiInformationLine,
        RiAddLine,
        RiCloudLine,
        RiUploadCloudLine,
        RiUploadCloud2Line,
        RiDownloadCloudLine,
        RiDownloadCloud2Line,
        RiSaveLine,
        RiFileUploadLine,
        RiCheckboxCircleLine,
        RiCheckboxMultipleLine,
        RiLock2Fill,
        RiLockLine,
        RiCloseLine,
        RiErrorWarningLine,
        RiFilterLine,
        RiFileCopyLine,
        RiFolderOpenLine,
        RiSettings3Line,
        RiFileList3Line,
        RiFileSettingsLine,
        RiFileDownloadLine,
        RiArrowRightLine,
        RiAlarmWarningLine,
        RiGitMergeLine,
        RiMore2Fill,
        RiFileEditLine,
        RiEditLine,
        RiGitCommitLine,
        RiFileTextLine,
        RiDeleteBin5Line,
        RiPlayListAddLine,
        RiCornerLeftUpLine,
        RiExternalLinkLine,
        RiArrowUpCircleLine,
        RiPaletteLine,
        RiSubtractLine,
        RiSendPlane2Line,
        RiEqualLine,
        RiNotificationLine,
        RiCoinLine,
        RiBookOpenLine,
        RiQuestionnaireLine,
        RiDiscordLine,
        RiGithubLine,
        RiTwitterXLine,
        RiArrowUpSLine,
        RiEarthLine,
        RiRepeat2Line,
        RiArrowUpDownLine,
        RiCornerLeftUpLine,
        RiPushpinLine,
        RiUnpinLine,
        RiSparklingLine,
        RiLink,
        RiSuitcase2Line,
        RiHome3Line,
        RiLeafLine,
        RiSwapBoxLine,
        RiSeedlingLine,
        RiCopyrightLine,
        RiTokenSwapLine,
        RiPercentLine,
        RiShakeHandsLine,
        RiGitBranchLine,
        RiArrowLeftRightLine,
        RiArrowDownLine,
        RiArrowGoForwardLine,
        RiArrowGoBackLine,
        RiLockUnlockLine,
        RiHandCoinLine,
        RiRocketLine,
        RiRocket2Line,
        RiGovernmentLine,
        RiHandHeartLine,
        RiHeart2Line,
        RiLoopRightLine,
        RiCheckDoubleLine,
        RiGift2Line,
        RiDropFill,
        RiContrastDropFill,
        RiFileCloseLine,
        RiRefund2Line,
        RiFireLine,
        RiMedalLine,
        RiBox3Line,
        RiFileAddLine,
        RiPriceTagLine,
        RiListUnordered,
        RiFolderReduceLine,
        RiDownloadLine,
        RiBriefcaseLine,
        RiTrophyLine,
        RiCashLine,
        RiShareCircleLine,
        RiPriceTagLine,
        RiUploadLine,
        RiQuillPenLine,
        RiFileInfoLine,
        RiListCheck2,
        RiEarthLine,
        RiUser2Line,
        RiWifiLine,
        RiWifiOffLine,
        RiLoopLeftLine,
        RiBugLine,
        RiVirusLine,
        RiFileSearchLine,
        RiChatQuoteLine,
        RiArrowDownCircleLine,
        RiCalendarLine,
        RiDownloadCloudLine,
        RiSortAsc,
        RiSortDesc,
        RiAddBoxLine,
        RiCheckboxIndeterminateLine,
        RiFolderLine,
        RiUserSettingsLine,
        RiContactsLine,
        RiAdminLine,
        RiLayoutGridLine,
        RiSettings2Line,
        RiWaterPercentLine,
        RiEqualizerLine,
        RiUserLine,
        RiArchiveStackAddLine,
        RiArchiveStackReduceLine,
        RiCloudOffLine,
        RiCalendarLine,
        RiMapPinTimeLine,
        RiPushpinFill,
      ],
    },
    defaults,
  });
