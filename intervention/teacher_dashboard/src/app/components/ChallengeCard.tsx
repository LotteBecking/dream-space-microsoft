import { useState } from 'react';
import { X, CheckCircle, XCircle, Lightbulb } from 'lucide-react';
import { Challenge } from '../lib/challenges';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';

interface ChallengeCardProps {
  challenge: Challenge;
  onComplete: (correct: boolean) => void;
  onClose: () => void;
}

export default function ChallengeCard({ challenge, onComplete, onClose }: ChallengeCardProps) {
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [showResult, setShowResult] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);

  const handleSubmit = () => {
    if (selectedAnswer === null) return;
    
    const correct = selectedAnswer === challenge.correctAnswer;
    setIsCorrect(correct);
    setShowResult(true);
  };

  const handleClose = () => {
    if (showResult) {
      onComplete(isCorrect);
    }
    onClose();
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-100 text-green-700';
      case 'intermediate': return 'bg-yellow-100 text-yellow-700';
      case 'advanced': return 'bg-red-100 text-red-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <Badge className={getDifficultyColor(challenge.difficulty)}>
                  {challenge.difficulty}
                </Badge>
                <Badge variant="outline">{challenge.category}</Badge>
              </div>
              <CardTitle className="text-2xl">{challenge.title}</CardTitle>
              <CardDescription className="mt-1">{challenge.description}</CardDescription>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={handleClose}
              className="flex-shrink-0"
            >
              <X className="w-5 h-5" />
            </Button>
          </div>
        </CardHeader>

        <CardContent className="space-y-6">
          {!showResult ? (
            <>
              {/* Question */}
              <div className="bg-purple-50 border border-purple-200 rounded-lg p-6">
                <h3 className="font-semibold text-lg mb-2">Question:</h3>
                <p className="text-gray-700">{challenge.question}</p>
              </div>

              {/* Options */}
              <div className="space-y-3">
                <h3 className="font-semibold">Choose your answer:</h3>
                {challenge.options.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => setSelectedAnswer(index)}
                    className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                      selectedAnswer === index
                        ? 'border-purple-500 bg-purple-50'
                        : 'border-gray-200 hover:border-purple-300 hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                        selectedAnswer === index
                          ? 'border-purple-500 bg-purple-500'
                          : 'border-gray-300'
                      }`}>
                        {selectedAnswer === index && (
                          <div className="w-3 h-3 bg-white rounded-full" />
                        )}
                      </div>
                      <span>{option}</span>
                    </div>
                  </button>
                ))}
              </div>

              {/* Submit Button */}
              <Button
                onClick={handleSubmit}
                disabled={selectedAnswer === null}
                className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
                size="lg"
              >
                Submit Answer
              </Button>
            </>
          ) : (
            <>
              {/* Result */}
              <div className={`rounded-lg p-6 ${
                isCorrect ? 'bg-green-50 border-2 border-green-200' : 'bg-red-50 border-2 border-red-200'
              }`}>
                <div className="flex items-start gap-4">
                  {isCorrect ? (
                    <CheckCircle className="w-8 h-8 text-green-600 flex-shrink-0" />
                  ) : (
                    <XCircle className="w-8 h-8 text-red-600 flex-shrink-0" />
                  )}
                  <div>
                    <h3 className={`font-bold text-xl mb-2 ${
                      isCorrect ? 'text-green-800' : 'text-red-800'
                    }`}>
                      {isCorrect ? '🎉 Correct!' : '❌ Not quite right'}
                    </h3>
                    <p className={isCorrect ? 'text-green-700' : 'text-red-700'}>
                      {isCorrect 
                        ? `Great job! You earned ${challenge.points} points!` 
                        : `The correct answer was: ${challenge.options[challenge.correctAnswer]}`
                      }
                    </p>
                  </div>
                </div>
              </div>

              {/* Explanation */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                <div className="flex items-start gap-3">
                  <Lightbulb className="w-6 h-6 text-blue-600 flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="font-semibold text-blue-900 mb-2">Explanation:</h3>
                    <p className="text-blue-800">{challenge.explanation}</p>
                  </div>
                </div>
              </div>

              {/* Continue Button */}
              <Button
                onClick={handleClose}
                className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
                size="lg"
              >
                Continue
              </Button>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
