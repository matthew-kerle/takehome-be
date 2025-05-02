import React, { ReactNode } from 'react';
import {
  AppBar,
  Box,
  Container,
  Toolbar,
  Link as MuiLink,
  IconButton,
  Stack,
  Menu,
  MenuItem,
  Typography,
} from '@mui/material';
import AccountCircleOutlinedIcon from '@mui/icons-material/AccountCircleOutlined';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import { useState } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import logo from '../assets/bungalow-logo-dark.svg';

interface LayoutProps {
  children: ReactNode;
}

export const Layout = ({ children }: LayoutProps): React.ReactElement => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [profileAnchorEl, setProfileAnchorEl] = useState<null | HTMLElement>(null);
  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', backgroundColor: 'background.default' }}>
      <AppBar
        position="sticky"
        elevation={0}
        sx={{
          bgcolor: 'background.paper',
          color: 'text.primary',
          borderBottom: '1px solid #ececec',
          borderRadius: 0,
          top: 0,
          zIndex: 1100,
          height: 80,
        }}
      >
        <Toolbar sx={{ justifyContent: 'flex-start', minHeight: 80, height: 80, px: 3 }}>
          <MuiLink component={RouterLink} to="/" underline="none" sx={{ display: 'flex', alignItems: 'center', mr: 4 }}>
            <img src={logo} alt="Bungalow Logo" style={{ width: 160, height: 18.82, marginRight: 8 }} />
          </MuiLink>
          <Box sx={{ flexGrow: 1 }} />
          <Stack direction="row" spacing={3} alignItems="center" sx={{ mr: 1 }}>
            <Box>
              <MuiLink
                href="#"
                underline="none"
                color="inherit"
                sx={{
                  fontWeight: 700,
                  fontSize: 16,
                  px: 2,
                  py: 1.5,
                  borderRadius: 2,
                  transition: 'background 0.15s',
                  '&:hover, &:focus, &:active': {
                    backgroundColor: '#f5f5f5',
                  },
                }}
                onClick={handleMenu}
              >
                Renters
                <KeyboardArrowDownIcon sx={{ ml: 0.5, fontSize: 22, verticalAlign: 'middle' }} />
              </MuiLink>
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleClose}
                MenuListProps={{ sx: { p: 0 } }}
                PaperProps={{
                  sx: {
                    mt: 1,
                    minWidth: 200,
                    borderRadius: 2,
                    boxShadow: '0 4px 24px rgba(0,0,0,0.08)',
                    border: '1px solid #ececec',
                  },
                }}
              >
                <MenuItem
                  component="a"
                  href="https://bungalow.com/renters-rooms"
                  target="_blank"
                  rel="noopener noreferrer"
                  sx={{
                    fontWeight: 700,
                    fontSize: 18,
                    py: 2,
                    px: 3,
                    '&:hover': { backgroundColor: '#f5f5f5' },
                  }}
                  onClick={handleClose}
                >
                  Rooms
                </MenuItem>
                <MenuItem
                  component="a"
                  href="https://bungalow.com/renters-homes"
                  target="_blank"
                  rel="noopener noreferrer"
                  sx={{
                    fontWeight: 700,
                    fontSize: 18,
                    py: 2,
                    px: 3,
                    '&:hover': { backgroundColor: '#f5f5f5' },
                  }}
                  onClick={handleClose}
                >
                  Entire Homes
                </MenuItem>
              </Menu>
            </Box>
            <MuiLink
              href="https://bungalow.com/homeowners"
              underline="none"
              color="inherit"
              sx={{
                fontWeight: 700,
                fontSize: 16,
                px: 2,
                py: 1.5,
                borderRadius: 2,
                transition: 'background 0.15s',
                '&:hover, &:focus, &:active': {
                  backgroundColor: '#f5f5f5',
                },
              }}
              target="_blank"
              rel="noopener noreferrer"
            >
              Homeowners
            </MuiLink>
            <MuiLink
              href="https://bungalow.com/institutional-investor"
              underline="none"
              color="inherit"
              sx={{
                fontWeight: 700,
                fontSize: 16,
                px: 2,
                py: 1.5,
                borderRadius: 2,
                transition: 'background 0.15s',
                '&:hover, &:focus, &:active': {
                  backgroundColor: '#f5f5f5',
                },
              }}
              target="_blank"
              rel="noopener noreferrer"
            >
              Investors
            </MuiLink>
            <MuiLink
              href="https://bungalow.com/about"
              underline="none"
              color="inherit"
              sx={{
                fontWeight: 700,
                fontSize: 16,
                px: 2,
                py: 1.5,
                borderRadius: 2,
                transition: 'background 0.15s',
                '&:hover, &:focus, &:active': {
                  backgroundColor: '#f5f5f5',
                },
              }}
              target="_blank"
              rel="noopener noreferrer"
            >
              About
            </MuiLink>
          </Stack>
          <IconButton
            color="inherit"
            aria-label="account"
            size="large"
            onClick={(e) => setProfileAnchorEl(e.currentTarget)}
          >
            <AccountCircleOutlinedIcon fontSize="large" />
          </IconButton>
          <Menu
            anchorEl={profileAnchorEl}
            open={Boolean(profileAnchorEl)}
            onClose={() => setProfileAnchorEl(null)}
            MenuListProps={{ sx: { p: 0 } }}
            PaperProps={{
              sx: {
                mt: 1,
                minWidth: 200,
                borderRadius: 2,
                boxShadow: '0 4px 24px rgba(0,0,0,0.08)',
                border: '1px solid #ececec',
              },
            }}
          >
            <MenuItem disabled sx={{ fontWeight: 700, fontSize: 18, color: '#7b8794', py: 2, px: 3 }}>
              Account
            </MenuItem>
            <MenuItem
              component="a"
              href="https://bungalow.com/login?next=%2F&from=%2F"
              target="_blank"
              rel="noopener noreferrer"
              sx={{ fontWeight: 400, fontSize: 18, py: 2, px: 3 }}
              onClick={() => setProfileAnchorEl(null)}
            >
              Login
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>
      <Container component="main" maxWidth={false} sx={{ mt: 4, mb: 4, flex: 1, width: '90vw', maxWidth: '90vw', mx: 'auto' }}>
        {children}
      </Container>
      <Box component="footer" sx={{ py: 3, px: 2, mt: 'auto', bgcolor: 'background.paper', borderTop: '1px solid #ececec' }}>
        <Container maxWidth="sm">
          <Typography variant="body2" color="text.secondary" align="center">
            © {new Date().getFullYear()} Bungalow Living, Inc. All rights reserved.
          </Typography>
        </Container>
      </Box>
    </Box>
  );
}; 