# 火山引擎大模型录音文件识别API

> 知识点来源：火山引擎官方API文档（2026-03-08获取）
> 功能概述：高精度语音转文本服务，支持多语言、方言、高级分析功能

---

## 📚 目录

1. [核心功能与流程](#一核心功能与流程)
2. [API接口概览](#二api接口概览)
3. [提交任务接口详解](#三提交任务接口详解)
4. [查询结果接口详解](#四查询结果接口详解)
5. [请求参数详解](#五请求参数详解)
6. [高级功能配置](#六高级功能配置)
7. [返回结果解析](#七返回结果解析)
8. [错误码参考](#八错误码参考)
9. [使用示例](#九使用示例)
10. [集成到视频工作流](#十集成到视频工作流)

---

## 一、核心功能与流程

### 处理流程
```
提交任务 → 获取任务ID → 查询结果 → 获取转录文本
    ↓           ↓           ↓           ↓
HTTP POST   Task ID   HTTP POST   JSON结果
```

### 核心能力
- **多语言支持**：中英文、多种方言、多种外语
- **高级分析**：说话人分离、情绪检测、性别识别
- **后处理**：文本规范化、标点恢复、语义顺滑
- **定制化**：热词、敏感词过滤、上下文理解

---

## 二、API接口概览

### 1. 提交任务接口
- **地址**: `https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit`
- **方法**: HTTP POST
- **格式**: JSON in HTTP Body
- **认证**: 需要App Key、Access Token

### 2. 查询结果接口
- **地址**: `https://openspeech.bytedance.com/api/v3/auc/bigmodel/query`
- **方法**: HTTP POST
- **格式**: JSON in HTTP Body
- **认证**: 需要App Key、Access Token、任务ID

---

## 三、提交任务接口详解

### 请求头 (Header)
| Key | 说明 | Value示例 |
|-----|------|-----------|
| `X-Api-App-Key` | APP ID | `123456789` |
| `X-Api-Access-Key` | Access Token | `your-access-key` |
| `X-Api-Resource-Id` | 资源信息ID | `volc.bigasr.auc` 或 `volc.seedasr.auc` |
| `X-Api-Request-Id` | 任务ID (推荐UUID) | `67ee89ba-7050-4c04-a3d7-ac61a63499b3` |
| `X-Api-Sequence` | 发包序号 | `-1` |

### 请求体结构
```json
{
  "user": {
    "uid": "用户标识"
  },
  "audio": {
    "url": "音频链接",
    "format": "音频格式",
    "language": "语言代码",
    "rate": 采样率,
    "channel": 声道数
  },
  "request": {
    "model_name": "bigmodel",
    "enable_itn": true,
    "enable_punc": false,
    // 其他高级参数
  },
  "callback": "可选回调地址",
  "callback_data": "可选回调数据"
}
```

---

## 四、查询结果接口详解

### 请求头 (Header)
| Key | 说明 | Value示例 |
|-----|------|-----------|
| `X-Api-App-Key` | APP ID | `123456789` |
| `X-Api-Access-Key` | Access Token | `your-access-key` |
| `X-Api-Resource-Id` | 资源信息ID | `volc.bigasr.auc` 或 `volc.seedasr.auc` |
| `X-Api-Request-Id` | 任务ID (提交时获取) | `67ee89ba-7050-4c04-a3d7-ac61a63499b3` |

### 请求体
```json
{}
```
（查询时只需任务ID，body可为空JSON）

---

## 五、请求参数详解

### 1. 音频配置参数

| 参数 | 说明 | 必填 | 默认值 | 可选值 |
|------|------|------|--------|--------|
| `url` | 音频链接 | ✓ | - | HTTP/HTTPS链接 |
| `format` | 音频容器格式 | ✓ | - | `raw` / `wav` / `mp3` / `ogg` |
| `language` | 指定语言 | ✗ | 自动检测 | 见语言代码表 |
| `codec` | 音频编码格式 | ✗ | `raw` | `raw` / `opus` |
| `rate` | 采样率 | ✗ | `16000` | 整数 |
| `bits` | 采样点位数 | ✗ | `16` | `16` |
| `channel` | 声道数 | ✗ | `1` | `1`(mono) / `2`(stereo) |

### 2. 语言代码表
| 语言 | 代码 | 备注 |
|------|------|------|
| 英语 | `en-US` | 美式英语 |
| 日语 | `ja-JP` | 日语 |
| 印尼语 | `id-ID` | 印尼语 |
| 西班牙语 | `es-MX` | 墨西哥西班牙语 |
| 葡萄牙语 | `pt-BR` | 巴西葡萄牙语 |
| 德语 | `de-DE` | 德语 |
| 法语 | `fr-FR` | 法语 |
| 韩语 | `ko-KR` | 韩语 |
| 菲律宾语 | `fil-PH` | 菲律宾语 |
| 马来语 | `ms-MY` | 马来语 |
| 泰语 | `th-TH` | 泰语 |
| 阿拉伯语 | `ar-SA` | 沙特阿拉伯语 |

**不指定language时**：支持中英文、上海话、闽南语、四川话、陕西话、粤语自动识别

---

## 六、高级功能配置

### 1. 基础功能
| 参数 | 说明 | 默认值 | 效果 |
|------|------|--------|------|
| `enable_itn` | 文本规范化 | `true` | 数字、货币等转换 |
| `enable_punc` | 标点恢复 | `false` | 添加标点符号 |
| `enable_ddc` | 语义顺滑 | `false` | 删除不流畅部分 |
| `model_version` | 模型版本 | `310` | `400`模型效果更优 |

### 2. 说话人相关
| 参数 | 说明 | 默认值 | 限制 |
|------|------|--------|------|
| `enable_speaker_info` | 说话人聚类分离 | `false` | 10人以内效果较好 |
| `ssd_version` | SSD版本 | - | 需配合`enable_speaker_info`使用 |

### 3. 音频分析
| 参数 | 说明 | 默认值 | 输出 |
|------|------|--------|------|
| `show_utterances` | 输出分句信息 | `false` | 分句文本和时间戳 |
| `show_speech_rate` | 显示语速 | `false` | token/s |
| `show_volume` | 显示音量 | `false` | 分贝 |
| `enable_lid` | 语种识别 | `false` | 语种标签 |
| `enable_emotion_detection` | 情绪检测 | `false` | 情绪标签 |
| `enable_gender_detection` | 性别检测 | `false` | male/female |

### 4. 声道处理
| 参数 | 说明 | 默认值 | 效果 |
|------|------|--------|------|
| `enable_channel_split` | 双声道识别 | `false` | `channel_id`标记左右声道 |
| `vad_segment` | 使用VAD分句 | `false` | 静音检测分句 |
| `end_window_size` | 强制判停时间 | - | 300-5000ms |

### 5. 内容过滤与增强
| 参数 | 说明 | 默认值 | 功能 |
|------|------|--------|------|
| `sensitive_words_filter` | 敏感词过滤 | - | 过滤/替换敏感词 |
| `enable_poi_fc` | POI function call | `false` | 地图领域推荐词 |
| `enable_music_fc` | 音乐 function call | `false` | 音乐领域推荐词 |
| `boosting_table_name` | 热词词表 | - | 自学习平台配置 |
| `correct_table_name` | 替换词词表 | - | 自学习平台配置 |

### 6. 上下文支持
支持传入上下文信息提升识别准确率：
```json
"corpus": {
  "context": "{\"hotwords\":[{\"word\":\"热词1\"}, {\"word\":\"热词2\"}]}"
}
```
或
```json
"corpus": {
  "context": "{\"context_type\":\"dialog_ctx\",\"context_data\":[{\"text\":\"对话历史1\"},{\"image_url\":\"图片URL\"}]}"
}
```

**豆包录音文件识别模型2.0**：支持视觉上下文，可传入图片辅助识别（限制1张，500k以内）

---

## 七、返回结果解析

### 成功响应结构
```json
{
  "audio_info": {
    "duration": 3696
  },
  "result": {
    "text": "完整识别文本",
    "utterances": [
      {
        "text": "分句文本",
        "start_time": 0,
        "end_time": 1705,
        "definite": true,
        "words": [
          {
            "text": "字",
            "start_time": 1200,
            "end_time": 1400,
            "blank_duration": 0
          }
        ],
        "additions": {
          "speech_rate": 150,
          "volume": -20,
          "lid_lang": "speech_mand",
          "emotion": "neutral",
          "gender": "male"
        }
      }
    ]
  }
}
```

### 响应头信息
| Header | 说明 | 示例 |
|--------|------|------|
| `X-Tt-Logid` | 服务端logid | `202407261553070FACFE6D19421815D605` |
| `X-Api-Status-Code` | 状态码 | `20000000` (成功) |
| `X-Api-Message` | 状态信息 | `OK` |

---

## 八、错误码参考

| 错误码 | 含义 | 处理建议 |
|--------|------|----------|
| `20000000` | 成功 | - |
| `20000001` | 正在处理中 | 稍后重试查询 |
| `20000002` | 任务在队列中 | 等待处理 |
| `20000003` | 静音音频 | 重新提交任务 |
| `45000001` | 请求参数无效 | 检查参数完整性 |
| `45000002` | 空音频 | 检查音频文件 |
| `45000151` | 音频格式不正确 | 检查音频格式 |
| `550xxxx` | 服务内部处理错误 | 联系技术支持 |
| `55000031` | 服务器繁忙 | 稍后重试 |

---

## 九、使用示例

### Python示例（伪代码）
```python
import requests
import uuid
import json

# 配置信息
API_URL_SUBMIT = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
API_URL_QUERY = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"
APP_KEY = "your_app_key"
ACCESS_KEY = "your_access_key"
RESOURCE_ID = "volc.seedasr.auc"  # 使用2.0模型

# 生成任务ID
task_id = str(uuid.uuid4())

# 提交任务
headers = {
    "X-Api-App-Key": APP_KEY,
    "X-Api-Access-Key": ACCESS_KEY,
    "X-Api-Resource-Id": RESOURCE_ID,
    "X-Api-Request-Id": task_id,
    "X-Api-Sequence": "-1",
    "Content-Type": "application/json"
}

payload = {
    "user": {
        "uid": "test_user_001"
    },
    "audio": {
        "url": "https://example.com/audio.mp3",
        "format": "mp3",
        "language": "zh-CN"  # 中文
    },
    "request": {
        "model_name": "bigmodel",
        "enable_itn": True,
        "enable_punc": True,
        "enable_ddc": True,
        "enable_speaker_info": False
    }
}

response = requests.post(API_URL_SUBMIT, headers=headers, json=payload)
if response.status_code == 200:
    print(f"任务提交成功，任务ID: {task_id}")
    
    # 查询结果（需要轮询）
    import time
    for i in range(10):  # 最多尝试10次
        time.sleep(2)  # 每2秒查询一次
        
        query_headers = {
            "X-Api-App-Key": APP_KEY,
            "X-Api-Access-Key": ACCESS_KEY,
            "X-Api-Resource-Id": RESOURCE_ID,
            "X-Api-Request-Id": task_id,
            "Content-Type": "application/json"
        }
        
        query_response = requests.post(API_URL_QUERY, headers=query_headers, json={})
        
        if query_response.status_code == 200:
            result = query_response.json()
            status_code = query_response.headers.get("X-Api-Status-Code")
            
            if status_code == "20000000":  # 成功
                print("识别结果:", result.get("result", {}).get("text", ""))
                break
            elif status_code == "20000001":  # 处理中
                print(f"处理中... 尝试第{i+1}次")
                continue
            else:
                print(f"查询失败: {query_response.headers.get('X-Api-Message', '未知错误')}")
                break
```

### 最佳实践建议
1. **任务ID管理**: 使用UUID确保唯一性，妥善保存用于查询
2. **轮询策略**: 建议2-5秒查询一次，最多尝试10-20次
3. **错误处理**: 根据错误码采取相应措施
4. **音频预处理**: 确保音频格式、采样率符合要求
5. **上下文利用**: 有特定场景时传入上下文提升准确率

---

## 十、集成到视频工作流

### 视频字幕生成流程
```
原始视频 → 提取音频 → 语音识别 → 生成字幕文件 → 合成带字幕视频
   ↓          ↓           ↓           ↓              ↓
.mp4/.mov   .mp3/.wav   文本转录    .srt/.ass      最终成品
```

### 应用场景

#### 1. 自动化字幕生成
```python
# 伪代码：视频转字幕工作流
def generate_subtitles_from_video(video_path):
    # 1. 提取音频
    audio_path = extract_audio(video_path)
    
    # 2. 语音识别
    text_result = volcengine_speech_recognition(audio_path)
    
    # 3. 生成字幕文件
    subtitles = create_srt_file(text_result, time_alignment=True)
    
    # 4. 可选：翻译字幕（结合翻译API）
    translated_subtitles = translate_subtitles(subtitles, target_lang="en")
    
    return subtitles, translated_subtitles
```

#### 2. 视频内容分析
- **关键词提取**: 从转录文本中提取关键词
- **情感分析**: 结合情绪检测功能分析视频情感倾向
- **说话人分析**: 多人对话场景分析各发言人内容
- **内容摘要**: 基于文本生成视频内容摘要

#### 3. 多语言视频处理
- **自动翻译**: 转录后自动翻译为目标语言
- **方言识别**: 识别视频中的方言内容
- **字幕同步**: 多语言字幕同步生成

### 配置建议

#### 视频字幕最佳配置
```json
{
  "request": {
    "model_name": "bigmodel",
    "model_version": "400",  // 使用400模型获得更好效果
    "enable_itn": true,      // 文本规范化
    "enable_punc": true,     // 标点恢复（字幕需要）
    "enable_ddc": true,      // 语义顺滑
    "show_utterances": true  // 获取分句和时间信息
  }
}
```

#### 会议录音分析配置
```json
{
  "request": {
    "model_name": "bigmodel",
    "enable_speaker_info": true,  // 说话人分离
    "enable_emotion_detection": true,  // 情绪分析
    "enable_gender_detection": true,   // 性别识别
    "show_speech_rate": true,          // 语速分析
    "show_volume": true                // 音量分析
  }
}
```

### 性能优化

1. **音频预处理**:
   - 转换到支持格式（mp3/wav）
   - 调整采样率到16000Hz
   - 单声道处理（channel: 1）

2. **批量处理**:
   - 多个音频文件批量提交
   - 异步处理，轮询结果
   - 结果缓存，避免重复识别

3. **错误恢复**:
   - 网络超时重试
   - 服务繁忙等待
   - 结果验证与修复

---

## 📊 性能指标参考

| 指标 | 说明 | 典型值 |
|------|------|--------|
| **识别准确率** | 中文普通话 | 95%+ |
| **处理速度** | 音频时长:处理时长 | 1:0.3-0.5（约2-3倍速）|
| **并发限制** | 同时处理任务数 | 依赖服务配额 |
| **音频限制** | 单文件大小 | 建议≤500MB |
| **音频时长** | 单文件时长 | 建议≤4小时 |

---

## 🔧 故障排除

### 常见问题与解决方案

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| **提交失败** | 认证信息错误 | 检查App Key/Access Token |
| **长时间处理中** | 音频过长/复杂 | 增加轮询间隔，检查音频格式 |
| **识别准确率低** | 音频质量差/背景噪音 | 音频预处理，降噪处理 |
| **分句不准确** | 语速过快/停顿不明显 | 调整`end_window_size`参数 |
| **说话人混淆** | 多人声音相似 | 限制说话人数，优化音频 |

### 调试建议
1. **记录logid**: 保存`X-Tt-Logid`用于问题定位
2. **测试音频**: 使用标准测试音频验证服务状态
3. **参数调试**: 逐步调整高级参数观察效果
4. **版本选择**: 尝试不同模型版本（310 vs 400）

---

## 📚 相关资源

1. **官方文档**: https://www.volcengine.com/docs/6561/1354868
2. **Demo代码**: 官方提供的Python/Go/Java示例
3. **控制台**: 火山引擎控制台获取认证信息
4. **自学习平台**: 配置热词、替换词表
5. **错误码文档**: 完整的错误码说明

---

## 🎯 总结

火山引擎大模型录音文件识别服务提供了**企业级**的语音转文本能力，特别适合：

✅ **视频制作**: 自动化字幕生成，多语言支持
✅ **内容分析**: 情感、说话人、关键词分析
✅ **会议记录**: 多人对话转录与分析
✅ **语音存档**: 音频内容结构化存储

通过合理配置高级参数，可以针对不同场景优化识别效果，显著提升视频制作和工作效率。

---
_文档创建: 2026-03-08_
_数据来源: 火山引擎官方API文档_
_维护者: 贾维斯_
_适用场景: 视频制作、音频处理、内容分析_