# DEV_STATUS.md

# 当前开发状态

> 本文件用于记录项目当前实际开发状态。
>
> 与 CLAUDE.md 不同，本文件允许 Claude Code 持续修改。
>
> 扩充关卡前请先读第 8～11 节（风格规范、关卡设计规则、工具与流程），新关卡须遵守其中的约定以保持风格一致。

---

# 1. 当前版本

- 玩法：上下布局的「大家来找茬」（上 = 原图 A，下 = 修改图 B），点击不同处，错点扣时，有提示次数。
- 开局先选模式：
  - **A 通关模式**：每关独立计时（关卡 `timeLimit`，统一 60 s），按顺序打完全部关卡后显示「恭喜，您已通关！」并回到模式选择；超时可重新挑战或返回。
  - **B 生存模式**：总时间 `survivalTime`（180 s），每过一关 +`survivalBonusPerLevel`（10 s），过关后直接进入下一关；关卡用完后从第一关继续（新一轮）。时间用完或点「结束」后显示成绩（通过关数 / 找到不同数 / 坚持秒数），最佳纪录存在 PlayerPrefs（`fd.survival.bestLevels / bestDiffs`）。成绩通过 `FindDifferencesGame.SurvivalEnded` 事件发出，供今后接入排行榜。
  - A/B 各有关卡数组和「随机顺序」开关（`campaignRandomOrder / survivalRandomOrder`）：开启后每轮内每关只出现一次，下一轮重新打乱（新一轮第一关不会与上一轮最后一关相同）。
- 场景：`Assets/FindDifferences/Test77.unity`，对象 `FindDifferencesGame` 的 `levels`（A 模式）列表当前 **150 关**（Level06～Level135 + Level500～519，按场景顺序见第 4 节；500 起为新编号段，资源名不连续不影响游戏内「第 N 关」，它按场景顺序计数）；`survivalLevels`（B 模式）当前与 A 相同。
- Level01～05（早期扁平经典 / 童话立体风格）仍会生成资源，但**不在场景列表中**。
- 运行时全部 UI 由代码构建（竖屏 1080×1920 适配）；图片为 900×600 纹理。
- 调试：`debugMode` 打开时画面显示「跳过本关 ▶」按钮（不加时、不弹结算）；`startLevel` 为 A 模式的起始关序号（随机顺序时无效；当前值由使用者在 Inspector 中设置，生成脚本不会改动）。

---

# 2. 当前主要目标

```
持续按主题扩充关卡，保持统一的纸艺（paper-craft）画风、满幅构图（无大片留白）、
每关 3～5 处清晰、互相隔开的不同，并合理使用动态元素 / 昼夜 / 天气系统。
```

---

# 3. 当前任务

- 无进行中的任务（最近一次：新增城市日常主题第二组 Level510～519（水族馆 / 马戏团 / 花店 / 建筑工地 / 火车站台 / 恐龙博物馆 / 雨天街角咖啡 / 南瓜农场 / 露天溜冰场 / 宠物店），已加入 A、B 两个模式的关卡列表。上一次：Level500～509，`diff_select.py` 的关卡编号识别范围由 1～199 扩大到 1～999）。

---

# 4. 已完成

## 4.1 场景内关卡清单（按场景顺序）

序号 = 场景中的关卡顺序（玩家看到的第 N 关），「特性」列：昼夜 = day/night 循环，天气 = weather 循环，其他为特殊后处理或镜头。

| 序 | 资源 | 标题 | 生成模块 | 视角 / 风格要点 | 特性 |
|---|---|---|---|---|---|
| 1 | Level06 | 纸艺海港 | levels_paper | 侧视纸艺（基准关） | |
| 2 | Level07 | 纸艺秋林 | levels_paper | 侧视纸艺，日月轨道 | 昼夜 |
| 3 | Level08 | 纸艺野餐 | levels_topdown | 正俯视 | |
| 4 | Level09 | 纸艺小镇 | levels_topdown | 正俯视 | |
| 5 | Level10 | 纸艺地下 | levels_views | 侧面剖面 | |
| 6 | Level11 | 纸艺游乐园 | levels_views | 等距 45°（满幅地面） | |
| 7 | Level12 | 纸艺小屋 | levels_more | 正面剖面（娃娃屋） | |
| 8 | Level13 | 纸艺林冠 | levels_more | 仰视 | |
| 9 | Level14 | 纸艺窗外 | levels_more | 室内看窗外 | |
| 10 | Level15 | 纸艺雪村 | levels_more | 等距 | |
| 11 | Level16 | 纸艺田园 | levels_weather | 侧视 | 天气 |
| 12 | Level17 | 纸艺山村 | levels_weather | 等距 | 天气 |
| 13 | Level18 | 纸艺海滩 | levels_weather | 侧视 | 天气 |
| 14 | Level19 | 城堡要塞 | levels_medieval | 中世纪 | 昼夜 |
| 15 | Level20 | 中世纪集市 | levels_medieval | 中世纪（等距） | 天气 |
| 16 | Level21 | 酒馆内景 | levels_medieval | 中世纪室内 | 昼夜 |
| 17 | Level22 | 霓虹雨街 | levels_cyber | 赛博朋克 | 天气 / neon_post |
| 18 | Level23 | 天台都市 | levels_cyber | 赛博朋克（等距） | 昼夜 / 天气 / neon_post |
| 19 | Level24 | 霓虹十字路口 | levels_cyber | 赛博朋克 | 天气 / neon_post |
| 20 | Level25 | 樱花坂道 | levels_anime | 日式动漫 | 天气 / anime_post |
| 21 | Level26 | 夏祭神社 | levels_anime | 日式动漫（等距） | 昼夜 / anime_post |
| 22 | Level27 | 仰望夏空 | levels_anime | 日式动漫 仰视 | 天气 / anime_post |
| 23 | Level28 | 纸艺转盘村 | levels_orbit | 环绕镜头（3 视角 120°，6 s 切换，18 s 复位），手工桌面背景 | 环绕镜头 |
| 24 | Level29 | 蒸汽工坊 | themes1 | 蒸汽朋克 | 天气 |
| 25 | Level30 | 星际港口 | themes1 | 科幻 | 昼夜 |
| 26 | Level31 | 地下避难所 | themes1 | 剖面 | |
| 27 | Level32 | 荒漠公路 | themes1 | 荒漠 | 天气 |
| 28 | Level33 | 隔离区 | themes1 | 正俯视 | 天气 |
| 29 | Level34 | 科研实验室 | themes1 | 室内 | |
| 30 | Level35 | 水没都市 | themes2 | 洪水城市（基准关） | 天气 |
| 31 | Level36 | 热带雨林 | themes2 | | 天气 |
| 32 | Level37 | 极地冰原 | themes2 | | 昼夜 / 天气 |
| 33 | Level38 | 火山岛 | themes2 | | 天气 |
| 34 | Level39 | 深海 | themes2 | | |
| 35 | Level40 | 地下遗迹 | themes2 | 剖面 | |
| 36 | Level41 | 失落神殿 | themes3 | | 昼夜 |
| 37 | Level42 | 沉船 | themes3 | 舷窗第一人称 | |
| 38 | Level43 | 海盗船 | themes3 | | 天气 |
| 39 | Level44 | 沙漠绿洲 | themes3 | | 昼夜 / 天气 |
| 40 | Level45 | 西部小镇 | themes3 | | 昼夜 |
| 41 | Level46 | 港口酒馆 | themes3 | 室内 | 昼夜 |
| 42 | Level47 | 油画·麦田 | themes4 | 油画后处理 | oil_post |
| 43 | Level48 | 素描·街角 | themes4 | 素描后处理 | sketch_post |
| 44 | Level49 | 动物小镇 | themes4 | 拟人动物 | |
| 45 | Level50 | 炼金工房 | themes4 | 室内 | |
| 46 | Level51 | 浮空群岛 | themes4 | | 昼夜 |
| 47 | Level52 | 妖精森林 | themes4 | | 昼夜 |
| 48 | Level53 | 巫师塔 | themes5 | 剖面 | |
| 49 | Level54 | 魔法学院 | themes5 | | 昼夜 |
| 50 | Level55 | 暗黑城堡 | themes5 | 暗黑幻想 | 天气 |
| 51 | Level56 | 倒置城市 | themes5 | 上下倒置 | |
| 52 | Level57 | 天空之城 | themes5 | 仰视 | |
| 53 | Level58 | 玩具城市 | themes5 | 等距（木地板） | |
| 54 | Level59 | 微缩世界 | themes5 | 正俯视移轴 | tiltshift_post |
| 55 | Level60 | 火车窗外 | levels_vehicle | 车窗视差滚动 | 昼夜 |
| 56 | Level61 | 夜行出租车 | levels_vehicle | 车窗视差滚动 | 天气 |
| 57 | Level62 | 飞机舷窗 | levels_vehicle | 舷窗 | 昼夜 |
| 58 | Level63 | 欢乐游乐园 | levels_classic2 | 透视纸艺 2.5D（近大远小） | |
| 59 | Level64 | 港口集市 | levels_classic2 | 透视纸艺 2.5D | |
| 60 | Level65 | 冬日雪村 | levels_classic2 | 透视纸艺 2.5D，远近两层雪 | |
| 61 | Level66 | 无尽走廊 | levels_horror | 心理恐怖，室内单点透视 3D | |
| 62 | Level67 | 童年卧室 | levels_horror | 心理恐怖，室内透视 | |
| 63 | Level68 | 无人晚宴 | levels_horror | 心理恐怖，室内透视 | |
| 64 | Level69 | 文艺复兴佛罗伦萨 | levels_europe | 15 世纪欧洲 | |
| 65 | Level70 | 威尼斯狂欢节 | levels_europe | 16 世纪 | 昼夜 |
| 66 | Level71 | 荷兰黄金时代 | levels_europe | 17 世纪 | 天气 |
| 67 | Level72 | 凡尔赛花园 | levels_europe | 18 世纪 | |
| 68 | Level73 | 维多利亚伦敦 | levels_europe | 19 世纪 | 昼夜 / 天气 |
| 69 | Level74 | 寝殿庭园 | levels_heian | 平安·大和绘 | |
| 70 | Level75 | 葵祭 | levels_heian | 平安 | |
| 71 | Level76 | 月夜舟游 | levels_heian | 平安 | 昼夜 |
| 72 | Level77 | 凤凰堂 | levels_heian2 | 平安 | |
| 73 | Level78 | 雪之晨 | levels_heian2 | 平安 | 天气（雪） |
| 74 | Level79 | 城下町 | levels_sengoku | 战国 | |
| 75 | Level80 | 川中岛 | levels_sengoku | 战国合战 | 天气（雾） |
| 76 | Level81 | 茶之汤 | levels_sengoku | 战国 剖面茶室 | |
| 77 | Level82 | 南蛮船 | levels_sengoku | 战国 | |
| 78 | Level83 | 夜之城 | levels_sengoku | 战国（夜间忍者） | 昼夜 |
| 79 | Level84 | 银座砖街 | levels_meiji | 明治 | 昼夜 |
| 80 | Level85 | 新桥驿 | levels_meiji | 明治 | |
| 81 | Level86 | 鹿鸣馆 | levels_meiji | 明治 | 昼夜 |
| 82 | Level87 | 横滨港 | levels_meiji | 明治 | 天气 |
| 83 | Level88 | 富冈制丝 | levels_meiji | 明治 | |
| 84 | Level89 | 日本桥 | levels_edo | 江户·浮世绘风味 | |
| 85 | Level90 | 神奈川冲浪里 | levels_edo | 浮世绘配色（普鲁士蓝 + 米色天空） | |
| 86 | Level91 | 歌舞伎小屋 | levels_edo | 剧场剖面 | |
| 87 | Level92 | 两国花火 | levels_edo | 江户 | 昼夜（烟花） |
| 88 | Level93 | 东海道宿场 | levels_edo | 江户 | 天气 |
| 89 | Level94 | 桃园结义 | levels_sanguo | 三国 | |
| 90 | Level95 | 赤壁之战 | levels_sanguo | 三国 | 昼夜（火光） |
| 91 | Level96 | 空城计 | levels_sanguo | 三国 | |
| 92 | Level97 | 三顾茅庐 | levels_sanguo | 三国 | 天气（雪） |
| 93 | Level98 | 草船借箭 | levels_sanguo | 三国 | 天气（雾） |
| 94 | Level99 | 长安西市 | levels_tangsong | 唐 | |
| 95 | Level100 | 清明上河图 | levels_tangsong | 宋 | |
| 96 | Level101 | 仕女游春 | levels_tangsong | 唐 | |
| 97 | Level102 | 西湖 | levels_tangsong | 宋 | 天气 |
| 98 | Level103 | 元宵灯会 | levels_tangsong | 宋 | 昼夜（灯会 / 烟花） |
| 99 | Level104 | 海的女儿 | levels_andersen | 安徒生童话 | |
| 100 | Level105 | 卖火柴的小女孩 | levels_andersen | 安徒生童话 | 天气（雪） |
| 101 | Level106 | 丑小鸭 | levels_andersen | 安徒生童话 | |
| 102 | Level107 | 皇帝的新装 | levels_andersen | 安徒生童话 | |
| 103 | Level108 | 拇指姑娘 | levels_andersen | 安徒生童话（巨物尺度） | |
| 104 | Level109 | 花果山 | levels_xiyou | 西游记 | |
| 105 | Level110 | 大闹天宫 | levels_xiyou | 西游记 | |
| 106 | Level111 | 三打白骨精 | levels_xiyou | 西游记 | |
| 107 | Level112 | 火焰山 | levels_xiyou | 西游记 | |
| 108 | Level113 | 通天河 | levels_xiyou | 西游记 | |
| 109 | Level114 | 秋叶原电器街 | levels_akiba | 秋叶原（无真实品牌） | 昼夜 |
| 110 | Level115 | 女仆咖啡厅 | levels_akiba | 室内 | |
| 111 | Level116 | 手办店 | levels_akiba | 室内 | |
| 112 | Level117 | 游戏中心 | levels_akiba | 室内（暗场霓虹） | |
| 113 | Level118 | 步行者天国 | levels_akiba | 街景 | |
| 114 | Level119 | 夜市擂台 | levels_misc | 街头格斗风格（原创角色 + HUD） | |
| 115 | Level120 | 黄昏码头 | levels_misc | 街头格斗风格（原创角色 + HUD） | |
| 116 | Level121 | 里斯本出航 | levels_misc | 大航海时代 | |
| 117 | Level122 | 新大陆登陆 | levels_misc | 大航海时代 | |
| 118 | Level123 | 纸艺露营地 | levels_oblique | 45° 伪 3D 俯视 + 光源投影 | |
| 119 | Level124 | 月下古堡 | levels_gothic | 哥特·吸血鬼城堡（夜景） | 天气（雾） |
| 120 | Level125 | 狼人之夜 | levels_gothic | 哥特·狼人（夜景） | 天气（雾） |
| 121 | Level126 | 伯爵大厅 | levels_gothic | 哥特·室内正面 | |
| 122 | Level127 | 城堡庭院 | levels_gothic | 中世纪城堡（白天） | 天气（雨） |
| 123 | Level128 | 午夜墓园 | levels_gothic | 哥特·墓园（夜景） | 天气（雷暴 / 雾） |
| 124 | Level129 | 肖像画廊 | levels_portrait | 画廊正面（古典肖像画 + 画家） | |
| 125 | Level130 | 体育比赛 | levels_modern | 足球场（看台观众、记分牌、球员） | |
| 126 | Level131 | 演唱会 | levels_modern | 夜间舞台（LED 墙、乐队、荧光棒人群，暗场 `dpiece`） | |
| 127 | Level132 | 大型展览 | levels_modern | 展馆室内（概念车转台、机械臂、地球仪） | |
| 128 | Level133 | 加油站 | levels_modern | 路边加油站（罩棚、油泵、价格牌、便利店、风车） | 昼夜 |
| 129 | Level134 | 商场 | levels_modern | 商场中庭（三层店铺、扶梯、喷泉） | |
| 130 | Level135 | 未来世界 | levels_modern | 未来城市（穹顶塔楼、磁悬浮、飞行车、机器人） | |
| 131 | Level500 | 动物园 | levels_daily | 侧视纸艺（长颈鹿、大象池、狮子岩、游客、气球、冰淇淋车） | |
| 132 | Level501 | 机场 | levels_daily | 航站楼室内 + 玻璃幕墙外停机坪（客机、塔台、航班信息屏） | |
| 133 | Level502 | 超市 | levels_daily | 室内（货架、水果摊、收银台、购物车） | |
| 134 | Level503 | 学校操场 | levels_daily | 钟楼校舍、秋千、滑梯、沙坑、篮球架 | |
| 135 | Level504 | 消防站 | levels_daily | 三车库消防站、消防车、晾水带塔、消防员、斑点狗 | |
| 136 | Level505 | 面包店 | levels_daily | 室内（面包架、黑板菜单、砖砌烤炉、蛋糕柜） | |
| 137 | Level506 | 湖畔公园 | levels_daily | 拱桥、凉亭、樱花树、划船、鸭子 | 天气（雨） |
| 138 | Level507 | 滑雪场 | levels_daily | 缆车、木屋、旗门、雪人、滑雪者 | 天气（雪 / 雾） |
| 139 | Level508 | 海边灯塔 | levels_daily | 悬崖灯塔、渔村、栈桥、帆船（夜间灯塔光束扫动） | 昼夜 |
| 140 | Level509 | 图书馆 | levels_daily | 室内（高书架 + 移动梯、拱窗、阅读桌、地球仪、睡猫） | |
| 141 | Level510 | 水族馆 | levels_daily2 | 暗场大厅 + 巨型水槽（珊瑚、鱼群、沉箱、水母） | |
| 142 | Level511 | 马戏团 | levels_daily2 | 帐篷室内（放射条纹、表演圈、空中秋千、象站鼓、小丑） | |
| 143 | Level512 | 花店 | levels_daily2 | 室内（阶梯花桶、吊篮、橱窗、花束柜台） | |
| 144 | Level513 | 建筑工地 | levels_daily2 | 塔吊、钢结构、脚手架、挖掘机、自卸车 | |
| 145 | Level514 | 火车站台 | levels_daily2 | 雨棚、停靠列车、时刻屏、站钟、自动售货机（远处快车驶过） | |
| 146 | Level515 | 恐龙博物馆 | levels_daily2 | 大厅（霸王龙骨架、展柜、讲解员与学生） | |
| 147 | Level516 | 雨天街角咖啡 | levels_daily2 | 咖啡馆外景（条纹遮阳篷、露天桌伞、自行车、打伞行人） | 天气（雨） |
| 148 | Level517 | 南瓜农场 | levels_daily2 | 秋季农场（谷仓、拖拉机、稻草人、南瓜田；夜间南瓜灯） | 昼夜 |
| 149 | Level518 | 露天溜冰场 | levels_daily2 | 小镇溜冰场（圣诞树、滑冰者、热可可摊、彩灯） | 天气（雪） |
| 150 | Level519 | 宠物店 | levels_daily2 | 室内（鱼缸、鸟笼、猫爬架、小狗围栏、仓鼠轮） | |

「基准关」：用户指定的满幅构图标准为场景序 1–5、9、13、20、22、30。

## 4.2 已实现的系统

- 动态元素 ElementAnim：bob/bounce、swing、rotate、pulse/stretch、twinkle、drift（含淡出 / 放大）、orbit（含景深 / 朝向）、spin（含明暗 / 快速翻面）、blink。
- 昼夜循环 DayNightCycle（元素可设为 Tinted / NightOnly / DayOnly / Untinted）。
- 天气循环 WeatherCycle：Clear / Overcast / Rain / Snow / Fog / Thunder / Heat，元素可按天气掩码显示。
- 环绕镜头 CameraOrbit（多视角帧切换，不同处随视角重新定位，转场时禁止点击）。
- 调试跳关按钮、错点冷却、提示。

---

# 5. 进行中

- 无。

---

# 6. 未开始

- 场景中尚未加入 Level01～05（早期风格，可按需决定是否加入或删除）。
- 45° 伪 3D 俯视（oblique）目前只有 Level123 一关，可作为新风格系列继续扩充。

---

# 7. 当前已知问题

- 有 32 关的部分不同是自动「换色」生成的（`diff_selection.json` 的 `auto`：把远离其他不同的一整块纸片换色；绿叶变秋色，太阳 / 月亮 / 光晕不参与）。如个别换色不够自然，可在关卡代码里改成手工设计的不同，再对该关运行 `diff_select.py measure` + `select`。
- `Tools~/Previews/` 下会残留动画检查脚本输出的 `*_anim.png`（Tools~ 不会被 Unity 导入，不影响构建）。
- 动态元素（云、鸟、漂移物）始终绘制在背景之上，若经过「不同」区域会暂时遮挡；新关卡需按第 9 节规则避免。

---

# 8. 画面风格规范（新关卡必须遵守）

## 8.1 基础风格：纸艺（paper-craft）

- 所有物件是「剪纸片」：`paper.piece(c, shapes, col, border, shadow)` —— 白色切边（`PAPER_WHITE`）+ 柔和投影；细节贴片用 `flat()`（无边无影）。
- 常用投影参数（kit.py）：`PROP=(2,4,7,0.42)` 物件，`SMALL=(1,2,3,0.3)` 小件，`LAYER=(1,3,11,0.36)` 大景片（山丘、地面层）。
- 景深用「分层景片」：天空渐变 → 远山（`layer()` / `hill_strip()`）→ 中景建筑 → 地面 → 前景人物/道具；远层颜色更淡、更偏天色。
- 所有图片最终做纸纹后处理 `post=paper_post`（含暗角）。特殊风格关可用 `oil_post / sketch_post / tiltshift_post / neon_post / anime_post`。
- 配色：明亮柔和、饱和度中等；暗场景（恐怖 / 夜景）可用 `paper25` 的 `edge_mix` 让切边随物体变色，避免发光白边。

## 8.2 视角变体（均保持纸艺质感）

| 视角 | 用法 / 工具 | 代表关 |
|---|---|---|
| 侧视（主力） | 分层景片、地面基线、人物站在 base y 上 | 大多数关 |
| 正俯视 | 地面铺满、物件看顶面 | Level08/09/33/59 |
| 等距 45° | `levels_views` 的 `P/iso_box/...` + `fill_iso`（地面铺满全画面，菱形外围补景物） | Level11/15/17/20/23/26/58 |
| 剖面（娃娃屋 / 地下） | 前墙切开显示室内 | Level10/12/31/40/53/81/91 |
| 仰视 / 倒置 | 消失点在上方 | Level13/27/56/57 |
| 透视纸艺 2.5D（近大远小） | `persp.View`（地平线 + 消失点，物体按地面深度缩放、远处入雾）+ `paper25`（基础图元自动转纸片） | Level63–65 |
| 室内单点透视 3D | `persp.Cam`（真实米制坐标、深度雾、墙面/地面/背墙平面绘制、`seven_seg` 墙面数字） | Level66–68 |
| 45° 伪 3D 俯视 + 光源投影 | `oblique.py`（顶面亮、正面暗；太阳左后上方，阴影落向右下：`SX=0.75, SY=-0.55` 每单位高度） | Level123 |
| 车窗 / 舷窗第一人称 | 窗框内视差滚动 `scroll()`、窗上雨滴 | Level42/60–62 |
| 环绕镜头 | `orbit3d.py` 多视角帧 | Level28 |

## 8.3 主题系列风格要点

- **欧洲 15–19 世纪**（levels_europe）：侧视纸艺，地标建筑做中景，人物带时代服饰（`lady / tricorne / top_hat / hat_cap`）。
- **日本**（levels_heian / heian2 / sengoku / meiji / edo + `jp_kit`）：平安用金色霞带 `kasumi`、桧皮弯曲屋顶 `curved_roof`、竹帘 `hall()`、十二单 `lady_seated`；战国用天守 `castle_keep`、町屋 `machiya`、武士 / 足轻；明治用红砖拱廊 `brick_front`、煤气灯、人力车、机车、汽船；江户带浮世绘配色（普鲁士蓝 `PRUSSIAN`）。
- **中国**（levels_sanguo / tangsong / xiyou + `cn_kit`）：曲线翘角屋顶 `cn_roof`、斗拱色带、殿堂 `cn_hall`、宝塔、城墙城楼、拱桥、灯笼；人物 `hanfu`（futou / wing / guan / tang_lady / lady / bun / straw）、武将 `warrior`（blade / snake / spear / sword）；西游四人 `wukong / tangseng / bajie / shaseng`。
- **童话**（levels_andersen）：明亮童话配色，可用尺度对比（拇指姑娘的巨物视角）。
- **城市日常**（levels_daily / levels_daily2，Level500～）：侧视纸艺，明亮日常配色；人物统一用 `modern()`，招牌 / 屏幕文字用 `sign_box()` 随机笔画；不同以「整件换色 / 整件增删」为主（灯具改为整个灯头换色，避免只换小灯芯导致像素不足）。
- **现代 / 秋叶原**（levels_akiba）：`modern()` 人物、`maid()`、`sign_box()` 竖排招牌（用随机笔画代替文字）、`chibi()` 手办；**不使用真实品牌、商标或现有角色**。
- **格斗游戏风格**（levels_misc）：原创格斗家（`fighter_gi / fighter_kungfu / wrestler`）+ 顶部血条 / 七段数字倒计时 HUD；**不复刻任何版权角色**。
- **心理恐怖**（levels_horror）：不血腥，靠「不对劲」营造氛围（空洞的眼、黑影、镜中人），深度雾 + 冷暖对比的光源。
- **哥特 / 中世纪怪物**（levels_gothic）：侧视纸艺；夜景用 `dpiece()`（切边改为暗紫 `NIGHT_EDGE`，避免发光白边），满月 `moon()`、尖拱 `gothic_arch()`、蝙蝠 `bat_el()`；原创角色 `vampire()`（高领披风，可张臂）、`werewolf()`（可仰头嚎叫）、`villager()`（火把 / 草叉，火焰为 `flame` 元素）、`knight()`；不血腥。白天的中世纪关（如城堡庭院）沿用普通白切边纸艺。

---

# 9. 关卡设计规则

- 画面 900×600（纹理像素，左上为原点绘制；`Difference` 资产里为左下原点，由生成器转换）。
- **满幅构图**：不得有大片空白天空 / 地面 / 墙面。远景补山、林、城市天际线、云带；前景补道具、植物、人物；室内补墙饰、家具；纯色区域不能透出画布黑底（天空渐变需覆盖到建筑缝隙）。
- **每关实际使用 3～5 处不同**。关卡代码里可以写更多「候选」（通常 7 处），由 `diff_select.py` 选出符合规则的 3～5 处（见 10.3）；类型以「颜色改变 / 物件增减 / 形状变化」为主，分散在画面各处。
- 不同的大小：每处变化像素 **≥ 400**（约 20×20 px 以上）；更小的候选不会被选用，应改为整件变色或整件增删。
- **任意两处不同的判定圈之间至少隔开画布宽度的 15%（135 px，圈边到圈边）**，不能重叠或相邻。
- 一个元素同时画多处不同时（例如室内整张前景贴图），用 `fdcore.on("id", m)` 代替 `m` 分别判断，否则这几处只能一起保留或一起舍弃。
- 不同处**不能被动态元素长期遮挡**：漂移云要限制在不同处上方的高度带；烟雾、飞鸟只做短暂经过；夜间才出现的元素（忍者、光晕）不放在不同处上。
- 不同处尽量放在**静态背景**中；放在动画元素上时用 `variant=True` 且动作幅度小（如轻微摇摆）。
- 夜间元素用 `daynight="night"`；发光物（火、灯）用 `"untinted"`；雾 / 云在昼夜关中改为 `"tinted"`，否则夜里会变成亮白块。
- 人物尺寸：侧视前景人物缩放 `h≈1.0–1.8`（约 45–80 px 高），主角可放大；不要让关键人物小于 40 px。
- 每关时限统一 60 秒（`fdcore.LEVEL_TIME_LIMIT`，关卡模块里写的时限不再生效）；动画时长 `anim_seconds` 与昼夜周期（40 s）或天气总时长对齐。
- 昼夜周期统一 40 s；天气步长 5～12 s、过渡 `blend=3.0`。
- 版权：只用公共领域题材或原创设计；现代场景不出现真实品牌。

---

# 10. 工具与生成流程

## 10.1 目录

- `Scripts/`：`FindDifferencesGame.cs`（游戏流程 / UI / 调试按钮）、`DifferencePicture.cs`（图片、元素动画、昼夜 / 天气着色、环绕镜头）、`FindDifferencesLevel.cs`（关卡 ScriptableObject、ElementAnim、DayNight / Weather / Orbit 数据）。
- `Art/`、`Levels/`：生成的图片与关卡资产（勿手改，改生成脚本后重新生成）。
- `Tools~/`（Unity 不导入）：Python 生成器。

## 10.2 生成器

```
cd Assets/FindDifferences/Tools~
python generate_assets.py Level123            # 生成指定关（资产写入 Art/ 与 Levels/）
python generate_assets.py Level123 --preview=<目录>   # 同时输出 A/B 对照预览并做自动核对
python generate_assets.py Level123 --anim=<目录>      # 输出动画 APNG
```

- 关卡定义：每个模块导出 `LEVELS = [(name, title, background(c, d), elements, diffs, time_limit, opts), ...]`，在 `generate_assets.py` 中 import 并加入 `ALL_LEVELS`。
- `background(c, d)`：`d` 为 B 图中生效的不同 id 集合，用 `"xxx" in d` 切换 A/B 内容。
- `diffs`：`(id, x, y, r)`；**`r=0` 表示自动拟合**（按 A/B 实际差异像素计算判定圈，搜索半径 170 px）——新关一律用 0，只有纯动画差异才手填半径。
- `elements`：`fdcore.E(id, draw(c, m), bbox=None, pivot=None, anim, animB, show="both|A|B", variant, daynight, weather)`。
- opts：`post`、`day_night=dict(period, phase, tint)`、`weather=dict(steps=[(TYPE, sec)...], blend, tints)`、`anim_seconds`、`frames`、`custom`（自定义构建器，如环绕镜头）。
- 资源 GUID 固定：`md5("FindDifferences/" + 相对路径)`，重复生成不会改变引用。

## 10.3 选择不同（diff_select.py）

```
python diff_select.py measure [LevelXX ...]   # 逐个候选单独测量（判定圈、像素数、由哪个元素绘制）-> diff_stats.json
python diff_select.py select [LevelXX ...]    # 按规则选出 3～5 处 -> diff_selection.json（不足 3 处时自动加「换色」不同）
python diff_select.py verify                  # 检查已生成的 Levels/*.asset（数量、间隔，环绕镜头关按每个视角）
```

- `generate_assets.py` 生成关卡时读取 `diff_selection.json`：只保留选中的不同（用测量出的判定圈，不再重新拟合），只画了被舍弃不同的元素在 A/B 中变为一致（`neutral`），`auto` 为换色不同。不在该文件中的关卡保持代码里的全部不同。
- 修改关卡的候选不同后：`measure` + `select` 该关，再重新生成。
- Level28（环绕镜头）不经过此流程，使用的不同在 `levels_orbit.py` 的 `USED28` 中手动指定（三个视角下都需满足间隔）。

## 10.4 自动核对（每次生成必看）

预览运行会打印：`check LevelXX: id=像素数 ...`
- 出现 `!! N stray px in [box]` = 有不在任何判定圈内的差异 → 修正（通常把该处改为 `r=0` 或调整提示点）。
- 某 id 为 `0` = 该不同在静态画面中看不见（被遮挡或只存在于动画）→ 检查绘制顺序 / 位置。
- 像素数过小（< ~150）→ 加大变化。
- 生成后需看预览图（A/B 上下拼接，B 图画出判定圈）确认构图与遮挡；有昼夜 / 天气的关再看动画帧。

## 10.5 加入场景

把 `Levels/LevelXX.asset` 的 GUID（`fdcore.guid_for("Levels/LevelXX.asset")`）追加到 `Test77.unity` 中 `FindDifferencesGame` 的 `levels:` 列表末尾（`- {fileID: 11400000, guid: <guid>, type: 2}`）；如该关也用于生存模式，同样追加到 `survivalLevels:` 列表末尾。不要改动 `startLevel / debugMode` 及两个随机开关的现值。
- `diff_select.py` 只读取 `levels:` 到 `startLevel:` 之间的 GUID（A 模式列表），所以脚本里这两个字段须保持名字和相邻顺序；只放在 `survivalLevels` 里的关卡不会被它处理。

## 10.6 共享库一览

| 模块 | 内容 |
|---|---|
| `fdcore.py` | Canvas 光栅化、着色器、元素 / 资产写出、动画求值、预览、自动拟合与核对 |
| `paper.py` | 纸片形状（Ell/Circ/RRect/Poly/Thick）、`piece / flat / soft_union`、`hill_strip`、纸纹后处理 |
| `kit.py` | 通用道具库（树、房、人物、拟人动物、云、鸟、烟、灯、后处理滤镜） |
| `stylekit.py` | 昼夜、日月、星空、火焰、窗光、霓虹 |
| `weather.py` | 雨、雪、雾、雷电、热浪、天气云 |
| `fills.py` / `fill_levels.py` / `fill_iso.py` | 去留白用的远景 / 前景 / 墙饰填充；等距关满幅地面 |
| `paper25.py` | 把普通绘图调用自动转换为纸片（按大小分层投影、上亮下暗、可选切边随色） |
| `persp.py` | `View` 地面透视（近大远小 + 雾）、`Cam` 室内 3D 透视、七段数字 |
| `oblique.py` | 45° 伪 3D 俯视 + 光源投影（box / cylinder / ball / cone / tent / figure / 树） |
| `jp_kit.py` | 日式建筑与人物（天守、町屋、鸟居、和服、武士、足轻、洋装、人力车、机车、汽船） |
| `levels_modern.py` 内 | `crowd()` 看台观众、`player()` 足球员、`car_side()` 侧视汽车、`pump()` 油泵（可供以后的现代题材复用） |
| `levels_daily.py` 内 | `giraffe / elephant / lion / dalmatian` 动物、`airliner()` 客机、`shelf_unit()` 超市货架、`bookcase()` 书架、`fire_truck()`、`firefighter()`、`skier()`、`snowman()`、`blossom_tree()`、`loaf()` 面包、`cake()`、`balloon_bunch()` 气球元素 |
| `levels_daily2.py` 内 | `coral()`、`big_fish()`、`bucket()` 花桶、`bloom()`、`worker()` 工人、`train_car()`、`trex()` 骨架、`umbrella()`、`pumpkin()`、`skater()` |
| `cn_kit.py` | 中式建筑与人物（屋顶、殿堂、宝塔、城墙城楼、拱桥、灯笼、汉服、武将、马、骆驼、帆船） |

---

# 11. 扩充新关卡的检查清单

1. 选定主题 → 选视角（默认侧视纸艺；系列内保持同一视角风格）。
2. 新建或沿用对应模块，复用第 10.5 节的共享库，保持比例与配色一致。
3. 构图满幅，安排 5～7 处分散、清晰的候选不同（`r=0`，每处 ≥ 400 px，彼此相隔 ≥ 135 px）。
4. 加入 2～6 个与主题相符的动态元素；需要时加昼夜或天气。
5. `diff_select.py measure / select` 该关 → `--preview` 生成，确认核对无 `!!`、`verify` 通过；查看预览图与动画帧。
6. 把关卡 GUID 追加到 `Test77.unity` 的 `levels` 列表末尾（diff_select 以该列表为准）。
7. 在本文件第 4.1 节表格追加一行，并更新「当前版本」中的关卡总数。
