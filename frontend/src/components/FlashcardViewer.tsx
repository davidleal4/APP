import { useState } from 'react'
import { Card, CardContent } from './ui/card'
import { Button } from './ui/button'
import { ChevronLeft, ChevronRight, RotateCcw, Check, X } from 'lucide-react'

interface Flashcard {
  id: string
  question: string
  answer: string
  difficulty: 'easy' | 'medium' | 'hard'
}

interface FlashcardViewerProps {
  flashcards: Flashcard[]
  onAnswer?: (cardId: string, correct: boolean) => void
}

export function FlashcardViewer({ flashcards, onAnswer }: FlashcardViewerProps) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [showAnswer, setShowAnswer] = useState(false)
  const [answeredCards, setAnsweredCards] = useState<Set<string>>(new Set())

  if (!flashcards.length) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-gray-500">No flashcards available</p>
      </div>
    )
  }

  const currentCard = flashcards[currentIndex]
  const isLastCard = currentIndex === flashcards.length - 1
  const isFirstCard = currentIndex === 0

  const handleNext = () => {
    if (!isLastCard) {
      setCurrentIndex(prev => prev + 1)
      setShowAnswer(false)
    }
  }

  const handlePrevious = () => {
    if (!isFirstCard) {
      setCurrentIndex(prev => prev - 1)
      setShowAnswer(false)
    }
  }

  const handleFlip = () => {
    setShowAnswer(!showAnswer)
  }

  const handleAnswer = (correct: boolean) => {
    if (onAnswer) {
      onAnswer(currentCard.id, correct)
    }
    setAnsweredCards(prev => new Set(prev).add(currentCard.id))
    
    // Auto advance to next card after answering
    setTimeout(() => {
      if (!isLastCard) {
        handleNext()
      }
    }, 500)
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100 text-green-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'hard': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const resetSession = () => {
    setCurrentIndex(0)
    setShowAnswer(false)
    setAnsweredCards(new Set())
  }

  return (
    <div className="max-w-2xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-4">
          <span className="text-sm text-gray-500">
            {currentIndex + 1} of {flashcards.length}
          </span>
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(currentCard.difficulty)}`}>
            {currentCard.difficulty}
          </span>
        </div>
        <Button variant="outline" size="sm" onClick={resetSession}>
          <RotateCcw className="h-4 w-4 mr-2" />
          Reset
        </Button>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-gray-200 rounded-full h-2 mb-6">
        <div 
          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
          style={{ width: `${((currentIndex + 1) / flashcards.length) * 100}%` }}
        />
      </div>

      {/* Flashcard */}
      <Card className="h-64 cursor-pointer mb-6" onClick={handleFlip}>
        <CardContent className="flex items-center justify-center h-full p-8">
          <div className="text-center">
            {showAnswer ? (
              <div>
                <p className="text-sm text-gray-500 mb-2">Answer:</p>
                <p className="text-lg font-medium">{currentCard.answer}</p>
              </div>
            ) : (
              <div>
                <p className="text-sm text-gray-500 mb-2">Question:</p>
                <p className="text-lg font-medium">{currentCard.question}</p>
                <p className="text-sm text-gray-400 mt-4">Click to reveal answer</p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Controls */}
      <div className="flex items-center justify-between">
        {/* Navigation */}
        <div className="flex items-center space-x-2">
          <Button 
            variant="outline" 
            size="sm" 
            onClick={handlePrevious}
            disabled={isFirstCard}
          >
            <ChevronLeft className="h-4 w-4 mr-1" />
            Previous
          </Button>
          <Button 
            variant="outline" 
            size="sm" 
            onClick={handleNext}
            disabled={isLastCard}
          >
            Next
            <ChevronRight className="h-4 w-4 ml-1" />
          </Button>
        </div>

        {/* Answer Buttons (shown when answer is revealed) */}
        {showAnswer && (
          <div className="flex items-center space-x-2">
            <Button 
              variant="outline" 
              size="sm" 
              onClick={() => handleAnswer(false)}
              className="text-red-600 border-red-200 hover:bg-red-50"
            >
              <X className="h-4 w-4 mr-1" />
              Incorrect
            </Button>
            <Button 
              variant="outline" 
              size="sm" 
              onClick={() => handleAnswer(true)}
              className="text-green-600 border-green-200 hover:bg-green-50"
            >
              <Check className="h-4 w-4 mr-1" />
              Correct
            </Button>
          </div>
        )}
      </div>

      {/* Session Summary (shown at the end) */}
      {isLastCard && answeredCards.size === flashcards.length && (
        <Card className="mt-6 bg-blue-50 border-blue-200">
          <CardContent className="text-center py-6">
            <h3 className="text-lg font-semibold text-blue-900 mb-2">
              Session Complete! 🎉
            </h3>
            <p className="text-blue-700">
              You've reviewed all {flashcards.length} flashcards.
            </p>
            <Button className="mt-4" onClick={resetSession}>
              Study Again
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}