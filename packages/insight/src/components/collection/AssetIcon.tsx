// Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
// This program is free software, you can redistribute it and/or modify it under the terms and conditions of
// CANN Open Software License Agreement Version 2.0 (the "License").
// Please refer to the License for details. You may not use this file except in compliance with the License.
// THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
// INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
// See LICENSE in the root of the software repository for the full text of the License.

// 资产图标（应用图标范式）：id 分两族——模型徽标（会话行用，图标跟模型
// 走：glm/deepseek/claude/openai…各品牌字标，白色 currentColor）与框架/
// 导入源徽标（最近导入用）。瓦色全站统一翡翠绿渐变（与品牌蓝、run 靛紫
// 三分互不撞色），唯 run 靛紫区分聚合层级。字标为自绘线性几何字形（24 网
// 格、圆角端点，无外部矢量库数据），与 lucide 图标同一视觉语言；调用侧传
// 归一后的 icon id（模型 id 由 modelIconId 从 Session.model 解析）。

import {
  BotIcon,
  LayersIcon,
  FlaskConicalIcon,
  BoxesIcon,
  FileJsonIcon,
  FileIcon,
  SparklesIcon,
} from 'lucide-react';
import type { ComponentType } from 'react';
import { cn } from '@/lib/utils';
import { displayModel } from '@/lib/collection/model-display';

export type AssetIconId =
  | 'glm'
  | 'deepseek'
  | 'claude'
  | 'openai'
  | 'gemini'
  | 'qwen'
  | 'kimi'
  | 'meta'
  | 'mistral'
  | 'xai'
  | 'minimax'
  | 'baidu'
  | 'tencent'
  | 'doubao'
  | 'huggingface'
  | 'model'
  | 'opencode'
  | 'cannbot'
  | 'dsh'
  | 'codex'
  | 'claude-code'
  | 'brand'
  | 'run'
  | 'jsonl'
  | 'unknown';

type GlyphProps = { className?: string };

// 线性字标公共笔触：与 lucide 同语言（宽 2 圆头），currentColor 单色渲染
const strokeGlyph = {
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 2,
  strokeLinecap: 'round',
  strokeLinejoin: 'round',
} as const;

// Claude——C 弧字标（开口朝右的单笔圆弧）
function ClaudeGlyph({ className }: GlyphProps) {
  return (
    <svg viewBox="0 0 24 24" {...strokeGlyph} className={className} aria-hidden="true">
      <path d="M17 7.8A6.5 6.5 0 1 0 17 16.2" />
    </svg>
  );
}

// OpenAI / Codex——六辐花字标（三线六十度交叉的放射花形）
function CodexGlyph({ className }: GlyphProps) {
  return (
    <svg viewBox="0 0 24 24" {...strokeGlyph} className={className} aria-hidden="true">
      <path d="M12 3v18M4.2 7.5l15.6 9M19.8 7.5l-15.6 9" />
    </svg>
  );
}

// opencode——代码括号字标（方括号对 + 光标点）
function OpencodeGlyph({ className }: GlyphProps) {
  return (
    <svg viewBox="0 0 24 24" {...strokeGlyph} className={className} aria-hidden="true">
      <path d="M9 5H6.5a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2H9M15 5h2.5a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H15" />
      <circle cx="12" cy="12" r="1.6" fill="currentColor" stroke="none" />
    </svg>
  );
}

// DeepSeek——D 弧字标（竖脊 + 右半圆）
function DeepSeekGlyph({ className }: GlyphProps) {
  return (
    <svg viewBox="0 0 24 24" {...strokeGlyph} className={className} aria-hidden="true">
      <path d="M6.5 4h4a8 8 0 0 1 0 16h-4Z" />
    </svg>
  );
}

// Gemini——四芒星字标（凹边十字闪光）
function GeminiGlyph({ className }: GlyphProps) {
  return (
    <svg viewBox="0 0 24 24" {...strokeGlyph} className={className} aria-hidden="true">
      <path d="M12 3q1.4 7.6 9 9q-7.6 1.4-9 9q-1.4-7.6-9-9q7.6-1.4 9-9Z" />
    </svg>
  );
}

// Qwen——Q 环字标（圆环 + 出环尾笔）
function QwenGlyph({ className }: GlyphProps) {
  return (
    <svg viewBox="0 0 24 24" {...strokeGlyph} className={className} aria-hidden="true">
      <circle cx="12" cy="12" r="6.5" />
      <path d="m16.2 16.2 4.3 4.3" />
    </svg>
  );
}

// Kimi——K 笔字标（竖脊 + 双斜笔）
function KimiGlyph({ className }: GlyphProps) {
  return (
    <svg viewBox="0 0 24 24" {...strokeGlyph} className={className} aria-hidden="true">
      <path d="M7 4v16M17.5 4l-9 8 9 8" />
    </svg>
  );
}

// GLM——Z 笔字标（双横 + 长斜连笔）
function GlmGlyph({ className }: GlyphProps) {
  return (
    <svg viewBox="0 0 24 24" {...strokeGlyph} className={className} aria-hidden="true">
      <path d="M5 5h14L5 19h14" />
    </svg>
  );
}

// Llama 系（Meta）——无限环字标（双圆相扣）
function MetaGlyph({ className }: GlyphProps) {
  return (
    <svg viewBox="0 0 24 24" {...strokeGlyph} className={className} aria-hidden="true">
      <circle cx="7.8" cy="12" r="4.6" />
      <circle cx="16.2" cy="12" r="4.6" />
    </svg>
  );
}

// Mistral——M 笔字标（双峰折线）
function MistralGlyph({ className }: GlyphProps) {
  return (
    <svg viewBox="0 0 24 24" {...strokeGlyph} className={className} aria-hidden="true">
      <path d="M5 20V4l7 9 7-9v16" />
    </svg>
  );
}

// Grok（xAI）——X 笔字标（交叉双斜线）
function XaiGlyph({ className }: GlyphProps) {
  return (
    <svg viewBox="0 0 24 24" {...strokeGlyph} className={className} aria-hidden="true">
      <path d="M5 4l14 16M19 4L5 20" />
    </svg>
  );
}

// MiniMax——双拱字标（小写 m 笔意）
function MinimaxGlyph({ className }: GlyphProps) {
  return (
    <svg viewBox="0 0 24 24" {...strokeGlyph} className={className} aria-hidden="true">
      <path d="M4 19v-8a4 4 0 0 1 8 0v8M12 11a4 4 0 0 1 8 0v8" />
    </svg>
  );
}

// 文心系（百度）——B 笔字标（竖脊 + 双层拱）
function BaiduGlyph({ className }: GlyphProps) {
  return (
    <svg viewBox="0 0 24 24" {...strokeGlyph} className={className} aria-hidden="true">
      <path d="M6.5 4v16M6.5 4h6.5a4 4 0 0 1 0 8H6.5M6.5 12h7.5a4 4 0 0 1 0 8h-7.5" />
    </svg>
  );
}

// 混元系（腾讯）——T 笔字标（冠横 + 脊竖）
function TencentGlyph({ className }: GlyphProps) {
  return (
    <svg viewBox="0 0 24 24" {...strokeGlyph} className={className} aria-hidden="true">
      <path d="M5 5h14M12 5v15" />
    </svg>
  );
}

// 豆包系（字节跳动）——律动条字标（三竖节拍，中位高）
function DoubaoGlyph({ className }: GlyphProps) {
  return (
    <svg viewBox="0 0 24 24" {...strokeGlyph} className={className} aria-hidden="true">
      <path d="M5.5 8.5v7M12 5v14M18.5 8.5v7" />
    </svg>
  );
}

// Hugging Face 托管模型——H 笔字标（双竖 + 腰横）
function HuggingFaceGlyph({ className }: GlyphProps) {
  return (
    <svg viewBox="0 0 24 24" {...strokeGlyph} className={className} aria-hidden="true">
      <path d="M6 4v16M18 4v16M6 12h12" />
    </svg>
  );
}

// 资产徽标统一瓦色：翡翠绿渐变（与品牌蓝、run 靛紫三分互不撞色）
const UNIFIED_GRAD = 'from-emerald-500 to-teal-600';

const ICONS: Record<AssetIconId, { Glyph: ComponentType<GlyphProps>; grad: string }> = {
  glm: { Glyph: GlmGlyph, grad: UNIFIED_GRAD },
  deepseek: { Glyph: DeepSeekGlyph, grad: UNIFIED_GRAD },
  claude: { Glyph: ClaudeGlyph, grad: UNIFIED_GRAD },
  openai: { Glyph: CodexGlyph, grad: UNIFIED_GRAD },
  gemini: { Glyph: GeminiGlyph, grad: UNIFIED_GRAD },
  qwen: { Glyph: QwenGlyph, grad: UNIFIED_GRAD },
  kimi: { Glyph: KimiGlyph, grad: UNIFIED_GRAD },
  meta: { Glyph: MetaGlyph, grad: UNIFIED_GRAD },
  mistral: { Glyph: MistralGlyph, grad: UNIFIED_GRAD },
  xai: { Glyph: XaiGlyph, grad: UNIFIED_GRAD },
  minimax: { Glyph: MinimaxGlyph, grad: UNIFIED_GRAD },
  baidu: { Glyph: BaiduGlyph, grad: UNIFIED_GRAD },
  tencent: { Glyph: TencentGlyph, grad: UNIFIED_GRAD },
  doubao: { Glyph: DoubaoGlyph, grad: UNIFIED_GRAD },
  huggingface: { Glyph: HuggingFaceGlyph, grad: UNIFIED_GRAD },
  model: { Glyph: SparklesIcon, grad: UNIFIED_GRAD },
  opencode: { Glyph: OpencodeGlyph, grad: UNIFIED_GRAD },
  cannbot: { Glyph: BotIcon, grad: UNIFIED_GRAD },
  dsh: { Glyph: LayersIcon, grad: UNIFIED_GRAD },
  codex: { Glyph: CodexGlyph, grad: UNIFIED_GRAD },
  'claude-code': { Glyph: ClaudeGlyph, grad: UNIFIED_GRAD },
  brand: { Glyph: FlaskConicalIcon, grad: UNIFIED_GRAD },
  run: { Glyph: BoxesIcon, grad: 'from-indigo-500 to-violet-600' },
  jsonl: { Glyph: FileJsonIcon, grad: UNIFIED_GRAD },
  unknown: { Glyph: FileIcon, grad: UNIFIED_GRAD },
};

// 模型串 → 徽标 id：先剥 provider 前缀（displayModel），再按主流品牌关键
// 字匹配；未知或缺失 → 通用模型徽标
export function modelIconId(model: string | null | undefined): AssetIconId {
  const m = (displayModel(model) ?? '').toLowerCase();
  if (!m) return 'model';
  if (m.includes('glm') || m.includes('chatglm') || m.includes('zhipu') || m.startsWith('z-')) return 'glm';
  if (m.includes('deepseek')) return 'deepseek';
  if (m.includes('claude')) return 'claude';
  if (m.includes('gemini')) return 'gemini';
  if (m.includes('qwen')) return 'qwen';
  if (m.includes('kimi') || m.includes('moonshot')) return 'kimi';
  if (m.includes('gpt') || m.includes('chatgpt') || m.includes('openai') || m.includes('codex') || /^o[134]\b/.test(m)) return 'openai';
  if (m.includes('grok') || m.includes('xai')) return 'xai';
  if (m.includes('llama') || m.includes('meta')) return 'meta';
  if (m.includes('mistral') || m.includes('mixtral') || m.includes('codestral') || m.includes('pixtral')) return 'mistral';
  if (m.includes('minimax') || m.includes('abab')) return 'minimax';
  if (m.includes('ernie') || m.includes('baidu') || m.includes('wenxin')) return 'baidu';
  if (m.includes('hunyuan') || m.includes('tencent')) return 'tencent';
  if (m.includes('doubao') || m.includes('skylark')) return 'doubao';
  if (m.includes('huggingface') || m.includes('hf.co') || m.startsWith('hf/')) return 'huggingface';
  return 'model';
}

export function AssetIcon({ id, className, size = 'md' }: { id: AssetIconId; className?: string; size?: 'md' | 'sm' }) {
  const cfg = ICONS[id] ?? ICONS.unknown;
  const { Glyph } = cfg;
  return (
    <span
      data-asset-icon={id}
      className={cn(
        'flex shrink-0 items-center justify-center rounded-[28%] bg-gradient-to-br text-white',
        'shadow-[0_1px_3px_rgba(0,0,0,0.18),0_6px_14px_-6px_rgba(0,0,0,0.28)]',
        size === 'md' ? 'size-10' : 'size-8',
        cfg.grad,
        className,
      )}
    >
      <Glyph className={size === 'md' ? 'size-[18px]' : 'size-[15px]'} />
    </span>
  );
}
