"use client";

import { ReactNode } from "react";

interface DashboardCardProps {
  title: string;
  value: string;
  subValue?: string;
  icon: ReactNode;
  color: string;
}

export default function DashboardCard({
  title,
  value,
  subValue,
  icon,
  color,
}: DashboardCardProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md border border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
            {title}
          </h3>
          <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
            {value}
          </div>
          {subValue && (
            <div className="text-sm text-gray-500 dark:text-gray-400">
              {subValue}
            </div>
          )}
        </div>
        <div className={`p-3 rounded-full ${color} text-white`}>{icon}</div>
      </div>
    </div>
  );
}
