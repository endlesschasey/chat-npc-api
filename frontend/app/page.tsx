import { ToastProvider } from '@/components/ui/toast'
import NPCDialogueSystem from '@/components/npc-dialogue'

export default function Home() {
  return (
    <ToastProvider>
      <NPCDialogueSystem />
    </ToastProvider>
  )
}