/**
 * Shared tool styling constants for MoneyMentor
 * Ensures consistent colors and icons across the UI
 */

export interface ToolStyle {
  gradient: string
  icon: string
  label: string
}

export const TOOL_STYLES: Record<string, ToolStyle> = {
  rag: {
    gradient: 'from-blue-500 to-purple-500',
    icon: '📚',
    label: 'RAG'
  },
  knowledge: {
    gradient: 'from-blue-500 to-purple-500',
    icon: '📚',
    label: 'Knowledge Base'
  },
  tavily: {
    gradient: 'from-indigo-500 to-blue-500',
    icon: '🔍',
    label: 'Tavily'
  },
  search: {
    gradient: 'from-indigo-500 to-blue-500',
    icon: '🔍',
    label: 'Web Search'
  },
  calculator: {
    gradient: 'from-green-500 to-emerald-500',
    icon: '🧮',
    label: 'Calculator'
  },
  default: {
    gradient: 'from-gray-500 to-gray-600',
    icon: '📄',
    label: 'Unknown'
  }
}

/**
 * Get tool style based on source name
 */
export const getToolStyle = (sourceName: string): ToolStyle => {
  const lowerSource = sourceName.toLowerCase()
  
  if (lowerSource.includes('knowledge') || lowerSource.includes('rag')) {
    return TOOL_STYLES.rag
  } else if (lowerSource.includes('tavily') || lowerSource.includes('search') || lowerSource.includes('web')) {
    return TOOL_STYLES.tavily
  } else if (lowerSource.includes('calculator') || lowerSource.includes('calculation')) {
    return TOOL_STYLES.calculator
  } else {
    return TOOL_STYLES.default
  }
}

/**
 * Get gradient for multi-tool suggestions
 */
export const getMultiToolGradient = (tools: string[]): string => {
  if (tools.length === 1) {
    return getToolStyle(tools[0]).gradient
  }
  
  // Multi-tool gradient for combined queries
  if (tools.length >= 3) {
    return 'from-orange-500 to-red-500'
  }
  
  // For 2 tools, use first tool's gradient
  return getToolStyle(tools[0]).gradient
}

