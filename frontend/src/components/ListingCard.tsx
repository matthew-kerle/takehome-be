import React from 'react';
import {
  Box,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Chip,
  Stack,
  IconButton,
  Tooltip,
  Link as MuiLink,
} from '@mui/material';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import BathtubIcon from '@mui/icons-material/Bathtub';
import HotelIcon from '@mui/icons-material/Hotel';
import SquareFootIcon from '@mui/icons-material/SquareFoot';
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';

interface ListingCardProps {
  image: string;
  price: string;
  address: string;
  beds: number;
  baths: number;
  sqft: number;
  year: number;
  soldDate: string;
  zillowUrl: string;
  type: string;
}

export const ListingCard: React.FC<ListingCardProps> = ({
  image,
  price,
  address,
  beds,
  baths,
  sqft,
  year,
  soldDate,
  zillowUrl,
  type,
}) => {
  return (
    <Card
      elevation={1}
      sx={{
        borderRadius: 4,
        overflow: 'hidden',
        minWidth: 300,
        maxWidth: 340,
        bgcolor: 'background.paper',
        boxShadow: '0 2px 12px rgba(0,0,0,0.04)',
        position: 'relative',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <Box sx={{ position: 'relative' }}>
        <CardMedia
          component="img"
          height="180"
          image={image}
          alt={address}
          sx={{ objectFit: 'cover' }}
        />
        <Chip
          label={type}
          size="small"
          sx={{ position: 'absolute', left: 12, bottom: 12, bgcolor: '#fff', color: 'text.primary', fontWeight: 600, fontSize: 13, px: 1.5, boxShadow: 1 }}
        />
        <Tooltip title="Save Listing">
          <IconButton
            sx={{ position: 'absolute', top: 10, right: 10, bgcolor: 'rgba(255,255,255,0.85)' }}
            size="small"
          >
            <FavoriteBorderIcon fontSize="small" color="action" />
          </IconButton>
        </Tooltip>
      </Box>
      <CardContent sx={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 1, pb: '16px !important' }}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <Typography variant="h6" sx={{ fontWeight: 700, fontSize: 22 }}>
            {price}
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 500 }}>
            Sold: {soldDate}
          </Typography>
        </Stack>
        <Typography variant="subtitle1" sx={{ fontWeight: 500, mb: 0.5 }}>
          {address}
        </Typography>
        <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 0.5 }}>
          <Stack direction="row" spacing={0.5} alignItems="center">
            <HotelIcon sx={{ fontSize: 18, color: 'primary.main' }} />
            <Typography variant="body2">
              {beds !== null ? beds : '—'} Beds
            </Typography>
          </Stack>
          <Stack direction="row" spacing={0.5} alignItems="center">
            <BathtubIcon sx={{ fontSize: 18, color: 'primary.main' }} />
            <Typography variant="body2">
              {baths !== null ? baths : '—'} Bath{baths !== 1 ? 's' : ''}
            </Typography>
          </Stack>
        </Stack>
        <Stack direction="row" spacing={2} alignItems="center">
          <Stack direction="row" spacing={0.5} alignItems="center">
            <SquareFootIcon sx={{ fontSize: 18, color: 'primary.main' }} />
            <Typography variant="body2">
              {sqft !== null ? `${sqft.toLocaleString()} sqft` : '— sqft'}
            </Typography>
          </Stack>
          <Stack direction="row" spacing={0.5} alignItems="center">
            <CalendarMonthIcon sx={{ fontSize: 18, color: 'primary.main' }} />
            <Typography variant="body2">
              Built {year !== null ? year : '—'}
            </Typography>
          </Stack>
        </Stack>
        <MuiLink
          href={zillowUrl}
          target="_blank"
          rel="noopener noreferrer"
          sx={{
            mt: 1.5,
            display: 'inline-block',
            fontWeight: 600,
            color: 'primary.main',
            fontSize: 15,
            textDecoration: 'none',
            '&:hover': {
              textDecoration: 'underline',
              color: 'secondary.main',
            },
          }}
        >
          View on Zillow
        </MuiLink>
      </CardContent>
    </Card>
  );
}; 