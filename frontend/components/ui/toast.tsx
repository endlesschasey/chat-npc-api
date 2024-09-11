'use client'

import React, { useState, useEffect, createContext, useContext, ReactNode } from 'react'

type ToastType = 'success' | 'error' | 'info'

export interface ToastContextType {
  showToast: (message: string, type: ToastType) => void
  hideToast: () => void
}

export const ToastContext = createContext<ToastContextType | undefined>(undefined)

export type ToastProps = {
  message: string
  type: ToastType
}

export type ToastActionElement = React.ReactElement<HTMLElement>

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toast, setToast] = useState<ToastProps | null>(null)

  const showToast = (message: string, type: ToastType = 'info') => {
    setToast({ message, type })
  }

  const hideToast = () => {
    setToast(null)
  }

  useEffect(() => {
    if (toast) {
      const timer = setTimeout(hideToast, 3000)
      return () => clearTimeout(timer)
    }
  }, [toast])

  return (
    <ToastContext.Provider value={{ showToast, hideToast }}>
      {children}
      {toast && (
        <div className={`fixed top-4 right-4 p-4 rounded shadow-lg ${
          toast.type === 'success' ? 'bg-green-500' :
          toast.type === 'error' ? 'bg-red-500' : 'bg-blue-500'
        } text-white`}>
          {toast.message}
        </div>
      )}
    </ToastContext.Provider>
  )
}

export function useToast() {
  const context = useContext(ToastContext)
  if (context === undefined) {
    throw new Error('useToast must be used within a ToastProvider')
  }
  return context
}