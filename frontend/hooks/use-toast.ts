import { useContext } from 'react'
import {
  ToastActionElement,
  ToastProps,
  ToastContext,
  ToastContextType // 确保导入了正确的类型
} from "../components/ui/toast"

export const useToast = (): ToastContextType => { // 确保返回正确的类型
  const context = useContext(ToastContext)
  if (context === undefined) {
    throw new Error('useToast must be used within a ToastProvider')
  }
  return context
}

export type Toast = ToastProps & {
  id: string
  title?: string
  description?: string
  action?: ToastActionElement
}