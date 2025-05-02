import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#00bfae', // Bungalow.com teal
      contrastText: '#fff',
    },
    secondary: {
      main: '#1a2233', // dark blue/navy for text/icons
    },
    background: {
      default: '#f7f8fa', // very light gray
      paper: '#fff',
    },
    text: {
      primary: '#222b45', // dark gray
      secondary: '#6b7280', // muted gray
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
    h1: {
      fontWeight: 700,
      fontSize: '2.5rem',
      color: '#222b45',
    },
    h2: {
      fontWeight: 600,
      fontSize: '2rem',
      color: '#222b45',
    },
    h5: {
      fontWeight: 500,
      color: '#222b45',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#fff',
          color: '#222b45',
          boxShadow: '0 2px 8px rgba(0,0,0,0.03)',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 16,
        },
      },
    },
  },
}); 