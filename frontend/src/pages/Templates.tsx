import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { FileText, Plus, Edit, Trash2, Eye, Copy } from 'lucide-react'
import { userApi } from '../lib/api'

export default function Templates() {
  const [showEditor, setShowEditor] = useState(false)
  const [currentTemplate, setCurrentTemplate] = useState<any>(null)
  const queryClient = useQueryClient()

  const { data: templates, isLoading } = useQuery({
    queryKey: ['cover-letters'],
    queryFn: async () => {
      const response = await userApi.listCoverLetters()
      return response.data.templates || []
    },
  })

  const handleNew = () => {
    setCurrentTemplate({
      template_name: 'New Template',
      content: 'Dear Hiring Manager at {{company}},\n\nI am writing to express my interest in the {{role}} position...',
      placeholders: { company: '', role: '', project: '', skill: '' }
    })
    setShowEditor(true)
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 flex items-center gap-3">
              <FileText className="h-10 w-10 text-purple-600" />
              Cover Letter Templates
            </h1>
            <p className="text-gray-600 mt-2 text-lg">
              Create reusable templates with smart placeholders
            </p>
          </div>
          <button
            onClick={handleNew}
            className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:shadow-lg transition font-semibold"
          >
            <Plus className="h-5 w-5" />
            New Template
          </button>
        </div>
      </div>

      {/* Templates Grid */}
      {isLoading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mb-4"></div>
          <p className="text-gray-600">Loading templates...</p>
        </div>
      ) : templates && templates.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {templates.map((template: any) => (
            <div
              key={template.id}
              className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 hover:shadow-xl transition"
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{template.template_name}</h3>
                  <p className="text-sm text-gray-500">Used {template.use_count} times</p>
                </div>
                <div className="flex gap-1">
                  <button className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg" title="Preview">
                    <Eye className="h-4 w-4" />
                  </button>
                  <button className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg" title="Edit">
                    <Edit className="h-4 w-4" />
                  </button>
                </div>
              </div>

              <div className="bg-gray-50 rounded-lg p-4 mb-4 text-sm text-gray-700 font-mono max-h-32 overflow-hidden">
                {template.content.substring(0, 150)}...
              </div>

              {/* Placeholders */}
              <div className="flex flex-wrap gap-2 mb-4">
                {Object.keys(template.placeholders || {}).map((key) => (
                  <span key={key} className="px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded-full">
                    {`{{${key}}}`}
                  </span>
                ))}
              </div>

              <div className="flex gap-2">
                <button className="flex-1 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 text-sm">
                  Use Template
                </button>
                <button className="p-2 text-purple-600 hover:bg-purple-50 rounded-lg">
                  <Copy className="h-4 w-4" />
                </button>
                <button className="p-2 text-red-600 hover:bg-red-50 rounded-lg">
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-lg p-12 text-center">
          <FileText className="h-16 w-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No Templates Yet</h3>
          <p className="text-gray-600 mb-6">Create your first cover letter template</p>
          <button
            onClick={handleNew}
            className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            Create Template
          </button>
        </div>
      )}

      {/* Editor Modal */}
      {showEditor && currentTemplate && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50">
          <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-2xl font-bold text-gray-900">Template Editor</h2>
            </div>

            <div className="p-6 space-y-4">
              {/* Template Name */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Template Name
                </label>
                <input
                  type="text"
                  value={currentTemplate.template_name}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                  placeholder="e.g., Data Scientist Application"
                />
              </div>

              {/* Content Editor */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Content (Use {{placeholder}} for variables)
                </label>
                <textarea
                  value={currentTemplate.content}
                  className="w-full h-64 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 font-mono text-sm"
                  placeholder="Dear Hiring Manager at {{company}}..."
                />
              </div>

              {/* Available Placeholders */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Available Placeholders
                </label>
                <div className="flex flex-wrap gap-2">
                  {['{{company}}', '{{role}}', '{{your_name}}', '{{project}}', '{{skill}}', '{{experience_years}}'].map((ph) => (
                    <button
                      key={ph}
                      className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm hover:bg-purple-200"
                    >
                      {ph}
                    </button>
                  ))}
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-3 justify-end pt-4 border-t border-gray-200">
                <button
                  onClick={() => setShowEditor(false)}
                  className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
                  Save Template
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tips Section */}
      <div className="mt-8 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl p-6 border border-purple-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">💡 Template Tips</h3>
        <ul className="space-y-2 text-gray-700">
          <li className="flex items-start gap-2">
            <span className="text-purple-600 mt-1">•</span>
            <span><strong>Use placeholders:</strong> {'{{company}}'} will be replaced with actual company name</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-purple-600 mt-1">•</span>
            <span><strong>Track success:</strong> Use count shows which templates work best</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-purple-600 mt-1">•</span>
            <span><strong>Be specific:</strong> Create different templates for different job types</span>
          </li>
        </ul>
      </div>
    </div>
  )
}
