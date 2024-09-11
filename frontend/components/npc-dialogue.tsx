'use client'

import React, { useState, useEffect, useRef, useCallback } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Card, CardContent } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import { useToast } from '../hooks/use-toast'
import { PlayIcon, PauseIcon, SendIcon, UserIcon, BotIcon, Loader2Icon, TrashIcon } from 'lucide-react'

const API_BASE_URL = 'http://192.168.30.144:8800'

type NPC = string
type Message = {
  id: string
  role: 'user' | 'npc'
  content: string
  audioId?: string
}

export default function NPCDialogueSystem() {
  const [npcs, setNpcs] = useState<NPC[]>([])
  const [selectedNPC, setSelectedNPC] = useState<NPC | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [conversationId, setConversationId] = useState<string | null>(null)
  const [playingAudioId, setPlayingAudioId] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isSending, setIsSending] = useState(false)
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const { toast } = useToast()

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [])

  const fetchNPCs = useCallback(async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/npc/list`)
      if (!response.ok) throw new Error('Failed to fetch NPCs')
      const data = await response.json()
      setNpcs(data)
    } catch (error) {
      console.error('Error fetching NPCs:', error)
      toast({ title: "Error", description: "Failed to load NPC list. Please try again.", variant: "destructive" })
    } finally {
      setIsLoading(false)
    }
  }, [toast])

  useEffect(() => {
    fetchNPCs()
  }, [fetchNPCs])

  useEffect(() => {
    scrollToBottom()
  }, [messages, scrollToBottom])

  const handleNPCSelect = (npc: NPC) => {
    setSelectedNPC(npc)
    setMessages([])
    setConversationId(null)
    setInput('')
  }

  const handleSendMessage = async () => {
    if (!input.trim() || !selectedNPC || isSending) return

    const userMessage: Message = { id: Date.now().toString(), role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsSending(true)

    try {
      const response = await fetch(`${API_BASE_URL}/npc/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: selectedNPC,
          message: input,
          conversation_id: conversationId,
          if_audio: true
        })
      })
      if (!response.ok) throw new Error('Failed to send message')
      const data = await response.json()
      const npcMessage: Message = { 
        id: Date.now().toString(),
        role: 'npc', 
        content: data.message, 
        audioId: data.audio_id 
      }
      setMessages(prev => [...prev, npcMessage])
      setConversationId(data.conversation_id)
    } catch (error) {
      console.error('Error sending message:', error)
      toast({ title: "Error", description: "Failed to send message. Please try again.", variant: "destructive" })
    } finally {
      setIsSending(false)
    }
  }

  const handlePlayAudio = async (audioId: string) => {
    if (playingAudioId === audioId) {
      audioRef.current?.pause()
      setPlayingAudioId(null)
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/npc/audio`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: selectedNPC,
          audio_id: audioId
        })
      })
      if (!response.ok) throw new Error('Failed to fetch audio')
      const data = await response.json()
      if (data.url) {
        if (audioRef.current) {
          audioRef.current.pause()
        }
        audioRef.current = new Audio(data.url)
        audioRef.current.play()
        setPlayingAudioId(audioId)
        audioRef.current.onended = () => setPlayingAudioId(null)
      }
    } catch (error) {
      console.error('Error playing audio:', error)
      toast({ title: "Error", description: "Failed to play audio. Please try again.", variant: "destructive" })
    }
  }

  const handleClearMessages = () => {
    setMessages([])
    setConversationId(null)
    toast({ title: "Success", description: "Message history cleared.", variant: "default" })
  }

  return (
    <div className="flex h-screen bg-gray-100">
      <div className="w-64 bg-white border-r shadow-sm">
        <ScrollArea className="h-full">
          <div className="p-4">
            <h2 className="mb-4 text-lg font-semibold text-primary">NPC List</h2>
            {isLoading ? (
              Array(5).fill(0).map((_, i) => (
                <Skeleton key={i} className="w-full h-10 mb-2" />
              ))
            ) : (
              npcs.map(npc => (
                <Button
                  key={npc}
                  variant={selectedNPC === npc ? 'default' : 'ghost'}
                  className="w-full justify-start mb-2 transition-colors"
                  onClick={() => handleNPCSelect(npc)}
                >
                  <BotIcon className="w-4 h-4 mr-2" />
                  {npc}
                </Button>
              ))
            )}
          </div>
        </ScrollArea>
      </div>
      <div className="flex-1 flex flex-col">
        <div className="p-4 bg-white border-b shadow-sm flex justify-between items-center">
          <h2 className="text-lg font-semibold">{selectedNPC ? `Chatting with ${selectedNPC}` : 'Select an NPC to start chatting'}</h2>
          <Button onClick={handleClearMessages} disabled={!selectedNPC || messages.length === 0} variant="outline">
            <TrashIcon className="w-4 h-4 mr-2" />
            Clear Chat
          </Button>
        </div>
        <ScrollArea className="flex-1 p-4">
          {messages.map((message) => (
            <Card key={message.id} className={`mb-4 ${message.role === 'user' ? 'ml-auto bg-primary text-primary-foreground' : 'mr-auto bg-secondary'} max-w-[70%]`}>
              <CardContent className="p-4">
                <div className="flex items-start gap-4">
                  <Avatar>
                    <AvatarFallback>{message.role === 'user' ? <UserIcon /> : <BotIcon />}</AvatarFallback>
                  </Avatar>
                  <div className="flex-1">
                    <p className="font-semibold mb-1">{message.role === 'user' ? 'You' : selectedNPC}</p>
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    {message.audioId && (
                      <Button
                        variant="outline"
                        size="sm"
                        className="mt-2"
                        onClick={() => handlePlayAudio(message.audioId!)}
                      >
                        {playingAudioId === message.audioId ? <PauseIcon className="w-4 h-4 mr-2" /> : <PlayIcon className="w-4 h-4 mr-2" />}
                        {playingAudioId === message.audioId ? 'Pause' : 'Play'} Audio
                      </Button>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
          <div ref={messagesEndRef} />
        </ScrollArea>
        <div className="p-4 bg-white border-t shadow-sm">
          <div className="flex gap-2">
            <Input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyPress={e => e.key === 'Enter' && handleSendMessage()}
              placeholder="Type your message..."
              disabled={!selectedNPC || isSending}
              className="flex-1"
            />
            <Button onClick={handleSendMessage} disabled={!selectedNPC || isSending}>
              {isSending ? (
                <Loader2Icon className="w-4 h-4 animate-spin" />
              ) : (
                <SendIcon className="w-4 h-4" />
              )}
              <span className="ml-2">Send</span>
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}