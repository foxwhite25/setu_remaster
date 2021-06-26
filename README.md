[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">setu-remaster</h3>
  <p align="center">
    瞎写的多线程涩图插件
    <br />
    <a href="https://github.com/foxwhite25/setu-remaster">查看本项目</a>
    ·
    <a href="https://github.com/foxwhite25/setu-remaster/issues">回报BUG</a>
    ·
    <a href="https://github.com/foxwhite25/setu-remaster/issues">请求功能</a>
  </p>
</p>




<!-- 目录 -->
<details open="open">
  <summary><h2 style="display: inline-block">目录</h2></summary>
  <ol>
    <li>
      <a href="#关于这个插件">关于这个插件</a>
      <ul>
        <li><a href="#特点">特点</a></li>
      </ul>
    </li>
    <li>
      <a href="#如何下载并且安装">如何下载并且安装</a>
      <ul>
        <li><a href="#必備條件">必備條件</a></li>
        <li><a href="#安装">安装</a></li>
      </ul>
    </li>
    <li><a href="#使用方法">使用方法</a></li>
    <li><a href="#未来规划">未来规划</a></li>
    <li><a href="#贡献">贡献</a></li>
    <li><a href="#协议">协议</a></li>
    <li><a href="#联系">联系</a></li>
    <li><a href="#致谢">致谢</a></li>
  </ol>
</details>



<!-- 关于这个插件 -->
## 关于这个插件
本插件使用pixivpy库直接从pixiv爬涩图，并使用多线程下载。
### 特点

* 采样数量保证质量
* 使用多线程下载，就算本地没有，50张涩图也只需要6秒钟




<!-- 如何安装 -->
## 如何下载并且安装

要得到一份本地副本，你只需要做以下这些简单的东西

### 必備條件

这个是一个<a href="https://github.com/Ice-Cirno/HoshinoBot/">Hoshino</a>插件，你必须要要有一个设置好的Hoshino。
* Hoshino
  ```sh
  git clone https://github.com/Ice-Cirno/HoshinoBot.git
  ```
### 安装

1. clone一份最新版本
2. 解压移动到modules文件夹
3. 在 `config/__bot__.py`的模块列表里加入 `setu_remaster`
4. 复制`config.default.json`为`config.json`并修改你要的东西。
```
{
  "randomness" : 1, # 随机性，默认1 (后来使用日期来随机寻找色图，所以1也不会出现大量重复)
  "multiply" : 3, # 采样倍数，色图采样数量总是30的倍数，例如用户要50张，3的话就会采样150张色图，并从中找出50张最好的，默认3
  "refresh_token" : "", # 刷新token , 查看https://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362/来获取
  "proxy" : "", # 访问梯子，推荐外置梯子。eg. http://app-api.pixivlite.com
  "daily_max" : 50, # 每日每人上限，默认50
  "freq_limit" : 5, # 频率限制，单位秒，默认5
  "default" : { # 群组默认设置
      "withdraw" : 0,  # 撤回时间，单位秒，0代表不撤回
      "xml": false, # 使用xml发图，可能因为风控无法发送，只支持go-cqhttp
      "foward" : true # 使用转发信息发图，可能因为风控无法发送，可以有效降低举报风险和刷屏数量
  }
}
```

<!-- USAGE EXAMPLES -->
## 使用方法

|指令|说明|
|-----|-----|
|涩图 |随机获取1张图片|
|来[n]张涩图 |随机获取[n]张图片|
|搜涩图 [keyword] |搜索指定关键字的图片|
|搜[n]张涩图 [keyword]|搜索[n]张指定关键字的图片|
|提取图片 [**id]|提取所有提供的[id]的图片|
|illust set [option] [key]|设置群独立设定|
|illust get |获取当前群的设定|



<!-- 未来规划 -->
## 未来规划
* 排行榜查看

<!-- 做出你的贡献 -->
## 做出你的贡献

贡献使开源社区成为了一个令人赞叹的学习，启发和创造场所。**非常感谢你所做的任何贡献**。

1. Fork 这个项目
2. 创建你的分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的改变 (`git commit -m '加入了超棒的功能'`)
4. Push到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个PR



<!-- LICENSE -->
## 协议

根据GPL3许可证分发。有关更多信息，请参见`LICENSE`。



<!-- CONTACT -->
## 联系

狐白白 - 1725036102 

项目地址: [https://github.com/foxwhite25/setu_remaster](https://github.com/foxwhite25/setu_remaster)



<!-- ACKNOWLEDGEMENTS -->
## 致谢

* []()<a href="https://github.com/Ice-Cirno/HoshinoBot/">Hoshino</a>




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/foxwhite25/setu_remaster.svg?style=for-the-badge
[contributors-url]: https://github.com/foxwhite25/setu_remaster/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/foxwhite25/setu_remaster.svg?style=for-the-badge
[forks-url]: https://github.com/foxwhite25/setu_remaster/network/members
[stars-shield]: https://img.shields.io/github/stars/foxwhite25/setu_remaster.svg?style=for-the-badge
[stars-url]: https://github.com/foxwhite25/setu_remaster/stargazers
[issues-shield]: https://img.shields.io/github/issues/foxwhite25/setu_remaster.svg?style=for-the-badge
[issues-url]: https://github.com/foxwhite25/setu_remaster/issues
[license-shield]: https://img.shields.io/github/license/foxwhite25/setu_remaster.svg?style=for-the-badge
[license-url]: https://github.com/foxwhite25/setu_remaster/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/foxwhite25
