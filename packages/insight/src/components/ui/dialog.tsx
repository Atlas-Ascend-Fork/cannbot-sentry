"use client"
// Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
// This program is free software, you can redistribute it and/or modify it under the terms and conditions of
// CANN Open Software License Agreement Version 2.0 (the "License").
// Please refer to the License for details. You may not use this file except in compliance with the License.
// THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
// INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
// See LICENSE in the root of the software repository for the full text of the License.

// 弹窗原语（@base-ui/react dialog 的薄封装）：DialogContent 自带 Portal +
// Backdrop 装配；side="right" 为右侧滑出抽屉形态（下钻/巡检类常驻阅读面），
// 缺省居中弹窗；showCloseButton 控制右上角关闭钮。data-slot 标记被样式与
// 测试选择器依赖，不可改名。

import * as React from "react"
import { Dialog as BaseDialog } from "@base-ui/react/dialog"
import { X as CloseMark } from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

// 遮罩：铺满暗幕 + 毛玻璃，开合各带淡入淡出
function DialogOverlay(props: BaseDialog.Backdrop.Props) {
  const { className, ...rest } = props
  return (
    <BaseDialog.Backdrop
      data-slot="dialog-overlay"
      className={cn(
        // 定位铺满与过渡基线
        "z-50 fixed inset-0 isolate bg-black/10 duration-100",
        // 毛玻璃（支持 backdrop-filter 的环境）与开合动效
        "supports-backdrop-filter:backdrop-blur-xs data-closed:fade-out-0 data-closed:animate-out data-open:fade-in-0 data-open:animate-in",
        className,
      )}
      {...rest}
    />
  )
}

// 根控制器
function Dialog(props: BaseDialog.Root.Props) {
  return <BaseDialog.Root data-slot="dialog" {...props} />
}

// 触发器
function DialogTrigger(props: BaseDialog.Trigger.Props) {
  return <BaseDialog.Trigger data-slot="dialog-trigger" {...props} />
}

// 传送门
function DialogPortal(props: BaseDialog.Portal.Props) {
  return <BaseDialog.Portal data-slot="dialog-portal" {...props} />
}

// 声明式关闭件
function DialogClose(props: BaseDialog.Close.Props) {
  return <BaseDialog.Close data-slot="dialog-close" {...props} />
}

// 头部纵排容器
function DialogHeader(props: React.ComponentProps<"div">) {
  const { className, ...rest } = props
  return <div data-slot="dialog-header" className={cn("flex flex-col gap-2", className)} {...rest} />
}

// 底部操作条：窄屏纵排倒序、宽屏右对齐横排，可选自带 Close 钮
function DialogFooter(props: React.ComponentProps<"div"> & { showCloseButton?: boolean }) {
  const { className, showCloseButton = false, children, ...rest } = props
  const trailingClose = showCloseButton ? (
    <BaseDialog.Close render={<Button variant="outline" />}>Close</BaseDialog.Close>
  ) : null
  return (
    <div
      data-slot="dialog-footer"
      className={cn(
        "flex flex-col-reverse gap-2 border-t bg-muted/50 p-4 sm:flex-row sm:justify-end -mx-4 -mb-4 rounded-b-xl",
        className,
      )}
      {...rest}
    >
      {children}
      {trailingClose}
    </div>
  )
}

// 标题
function DialogTitle(props: BaseDialog.Title.Props) {
  const { className, ...rest } = props
  return (
    <BaseDialog.Title
      data-slot="dialog-title"
      className={cn("font-heading font-medium text-base leading-none", className)}
      {...rest}
    />
  )
}

// 辅助说明（链接自动带下划线样式）
function DialogDescription(props: BaseDialog.Description.Props) {
  const { className, ...rest } = props
  return (
    <BaseDialog.Description
      data-slot="dialog-description"
      className={cn(
        "text-muted-foreground text-sm *:[a]:underline-offset-3 *:[a]:underline *:[a]:hover:text-foreground",
        className,
      )}
      {...rest}
    />
  )
}

// 内容主体：自动装配 Portal + 遮罩
function DialogContent(
  props: BaseDialog.Popup.Props & {
    showCloseButton?: boolean
    /** center = 居中弹窗（缺省）；right = 右侧滑出抽屉（inset-y 满高、左缘
     *  圆角 + 右滑入场——下钻/巡检类常驻阅读面） */
    side?: "center" | "right"
  },
) {
  const { className, children, showCloseButton = true, side = "center", ...rest } = props
  // 形态位：定位与圆角策略 + 入退场动效（center 缩放淡入，right 右滑）
  const positioning =
    side === "right"
      ? "inset-y-0 right-0 h-full max-w-full rounded-none rounded-l-xl border-l data-closed:slide-out-to-right data-closed:fade-out-0 data-closed:animate-out data-open:slide-in-from-right data-open:fade-in-0 data-open:animate-in"
      : "top-1/2 left-1/2 max-w-[calc(100%-2rem)] -translate-x-1/2 -translate-y-1/2 rounded-xl sm:max-w-sm data-closed:zoom-out-95 data-closed:fade-out-0 data-closed:animate-out data-open:zoom-in-95 data-open:fade-in-0 data-open:animate-in"
  // 右上角关闭钮（ghost 图标钮 + 屏幕阅读器文案）
  const closeButton = showCloseButton ? (
    <BaseDialog.Close
      data-slot="dialog-close"
      render={<Button variant="ghost" size="icon-sm" className="top-2 right-2 absolute" />}
    >
      <CloseMark />
      <span className="sr-only">Close</span>
    </BaseDialog.Close>
  ) : null
  return (
    <DialogPortal>
      <DialogOverlay />
      <BaseDialog.Popup
        data-slot="dialog-content"
        className={cn(
          // 弹层基线：铺满约束 + 弹层底色/描边
          "z-50 fixed grid w-full gap-4 bg-popover p-4 text-sm text-popover-foreground ring-1 ring-foreground/10 duration-100 outline-none",
          positioning,
          className,
        )}
        {...rest}
      >
        {children}
        {closeButton}
      </BaseDialog.Popup>
    </DialogPortal>
  )
}

export {
  // 根与装配
  Dialog,
  DialogTrigger,
  DialogPortal,
  DialogContent,
  DialogOverlay,
  DialogClose,
  // 结构件
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
}
