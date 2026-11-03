import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, it, expect } from 'vitest';
import LoginPage from '../pages/LoginPage';
import SettingsPage from '../pages/SettingsPage';

describe('CivicLens Frontend Tests', () => {
  it('renders login page correctly', () => {
    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    );
    expect(screen.getByText(/CivicLens Portal/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Sign In to Dashboard/i })).toBeInTheDocument();
  });

  it('renders settings profile form correctly', () => {
    render(
      <BrowserRouter>
        <SettingsPage />
      </BrowserRouter>
    );
    expect(screen.getByText(/Settings & Analyst Profile/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Save Profile Changes/i })).toBeInTheDocument();
  });
});

