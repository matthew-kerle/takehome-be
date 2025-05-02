import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Button,
  TextField,
  MenuItem,
  Stack,
  InputAdornment,
  Skeleton,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { ListingCard } from './components/ListingCard';
import TuneIcon from '@mui/icons-material/Tune';
import { AnimatePresence, motion } from 'framer-motion';

interface ApiListing {
  id: number;
  price: string;
  address: string;
  city: string;
  state: string;
  zipcode: string;
  bedrooms: number;
  bathrooms: number;
  home_size: number;
  year_built: number;
  last_sold_date: string;
  link: string;
  home_type: string;
}

const STOCK_IMAGES = [
  'https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?auto=format&fit=crop&w=400&q=80',
  'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80',
  'https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80',
  'https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=80',
  'https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?auto=format&fit=crop&w=400&q=80',
  'https://images.unsplash.com/photo-1465101178521-c1a9136a3b99?auto=format&fit=crop&w=400&q=80',
  'https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80',
  'https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=80',
];

const FRIENDLY_TYPE: Record<string, string> = {
  SingleFamily: 'Single Family',
  Apartment: 'Apartment',
  Condominium: 'Condominium',
  Miscellaneous: 'Miscellaneous',
  MultiFamily2To4: 'Multi-Family (2-4)',
  VacantResidentialLand: 'Vacant Residential Land',
};

const getFriendlyType = (type: string) => {
  if (FRIENDLY_TYPE[type]) {
    return FRIENDLY_TYPE[type];
  }
  // Split at uppercase letters, e.g. 'SingleFamily' -> 'Single Family'
  return type.replace(/([a-z])([A-Z])/g, '$1 $2');
};

export const HomePage: React.FC = () => {
  const [listings, setListings] = useState<ApiListing[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [page, setPage] = useState<number>(1);
  const [hasMore, setHasMore] = useState<boolean>(true);
  const [loadingMore, setLoadingMore] = useState<boolean>(false);

  const fetchListings = (pageNum: number, append = false) => {
    if (append) setLoadingMore(true);
    else setLoading(true);
    fetch(`/api/listings/?page_size=8&page=${pageNum}`)
      .then((res) => res.json())
      .then((data) => {
        if (append) {
          setListings((prev) => [...prev, ...(data.results || [])]);
        } else {
          setListings(data.results || []);
        }
        setHasMore(Boolean(data.next));
        setLoading(false);
        setLoadingMore(false);
      })
      .catch(() => {
        setLoading(false);
        setLoadingMore(false);
      });
  };

  useEffect(() => {
    fetchListings(1, false);
    setPage(1);
  }, []);

  const handleViewMore = () => {
    const nextPage = page + 1;
    setPage(nextPage);
    fetchListings(nextPage, true);
  };

  return (
    <Box sx={{ maxWidth: 900, mx: 'auto', pt: 8, pb: 6 }}>
      <Typography
        variant="h1"
        sx={{
          display: 'flex',
          alignItems: 'center',
          flexWrap: 'wrap',
          fontSize: { xs: '2.2rem', md: '3.2rem' },
          fontWeight: 800,
          lineHeight: 1.1,
          mb: 2,
          gap: 0,
        }}
      >
        Find your perfect
        <Box
          component="span"
          sx={{
            display: 'inline-flex',
            alignItems: 'center',
            background: '#fdded6',
            borderRadius: 1,
            px: 0.5,
            py: 0.5,
            ml: 2,
            minHeight: { xs: '2.2rem', md: '3.2rem' },
          }}
        >
          <Box
            component="span"
            sx={{
              background: 'linear-gradient(90deg, #ff6a00 0%, #ee0979 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
              color: 'transparent',
              fontWeight: 800,
              fontSize: { xs: '2.2rem', md: '3.2rem' },
              lineHeight: 1.1,
            }}
          >
            home
          </Box>
        </Box>
      </Typography>
      <Typography variant="h6" sx={{ color: 'text.secondary', mb: 4, fontWeight: 400 }}>
        Browse our curated selection of properties, from cozy bungalows to spacious family homes.
      </Typography>

      <Box sx={{ width: '100%', bgcolor: '#f7f8fa', py: 6, borderRadius: 4, mt: -4 }}>
        <Typography variant="h5" sx={{ fontWeight: 700, mb: 3, ml: 1 }}>
          Featured Listings
        </Typography>
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2.5} alignItems="center" mb={3} px={1}>
          <TextField
            variant="outlined"
            placeholder="Search by address, city, or zip code"
            sx={{
              flex: 2,
              minWidth: 260,
              bgcolor: '#fff',
              borderRadius: 2,
              '& .MuiOutlinedInput-root': {
                borderRadius: 2,
                fontSize: 20,
                fontWeight: 400,
                color: '#222b45',
                background: '#fff',
                height: 56,
                pl: 1.5,
              },
              '& .MuiInputAdornment-root svg': {
                color: '#222b45',
                fontSize: 26,
              },
            }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
          <TextField
            select
            variant="outlined"
            defaultValue="price-asc"
            sx={{
              flex: 1,
              minWidth: 200,
              bgcolor: '#fff',
              borderRadius: 2,
              '& .MuiOutlinedInput-root': {
                borderRadius: 2,
                fontSize: 20,
                fontWeight: 400,
                color: '#222b45',
                background: '#fff',
                height: 56,
                pl: 1.5,
              },
            }}
          >
            <MenuItem value="price-asc">Price (Low to High)</MenuItem>
            <MenuItem value="price-desc">Price (High to Low)</MenuItem>
            <MenuItem value="date-desc">Newest</MenuItem>
            <MenuItem value="date-asc">Oldest</MenuItem>
          </TextField>
          <Button
            variant="contained"
            startIcon={<TuneIcon sx={{ color: '#fff', fontSize: 26 }} />}
            sx={{
              minWidth: 180,
              height: 56,
              borderRadius: 2,
              background: 'linear-gradient(90deg, #ff914d 0%, #e94e77 100%)',
              color: '#fff',
              fontWeight: 700,
              fontSize: 20,
              boxShadow: 'none',
              px: 4,
              '&:hover': {
                background: 'linear-gradient(90deg, #ff914d 0%, #e94e77 100%)',
                opacity: 0.92,
              },
            }}
          >
            Filters
          </Button>
        </Stack>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2, ml: 1, fontSize: 16 }}>
          {loading ? 'Loading listings...' : `${listings.length} listings found`}
        </Typography>
        {loading ? (
          <Stack direction="row" spacing={3} flexWrap="wrap" useFlexGap px={1}>
            {[1,2,3,4].map((i) => (
              <Box key={i} sx={{ flex: '1 1 320px', maxWidth: 340, mb: 3 }}>
                <Skeleton variant="rectangular" width={340} height={180} sx={{ borderRadius: 4, mb: 2 }} />
                <Skeleton variant="text" width="60%" height={32} />
                <Skeleton variant="text" width="80%" height={24} />
                <Skeleton variant="text" width="40%" height={24} />
                <Skeleton variant="text" width="50%" height={24} />
              </Box>
            ))}
          </Stack>
        ) : (
          <>
            <Stack direction="row" spacing={3} flexWrap="wrap" useFlexGap px={1}>
              <AnimatePresence initial={false}>
                {listings.map((listing, idx) => (
                  <motion.div
                    key={listing.id}
                    initial={{ opacity: 0, y: 24 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 24 }}
                    transition={{ duration: 0.4, ease: 'easeOut' }}
                    style={{ flex: '1 1 320px', maxWidth: 340, marginBottom: 24 }}
                  >
                    <ListingCard
                      image={STOCK_IMAGES[idx % STOCK_IMAGES.length]}
                      price={listing.price}
                      address={`${listing.address}, ${listing.city}`}
                      beds={listing.bedrooms}
                      baths={listing.bathrooms}
                      sqft={listing.home_size}
                      year={listing.year_built}
                      soldDate={listing.last_sold_date}
                      zillowUrl={listing.link}
                      type={getFriendlyType(listing.home_type)}
                    />
                  </motion.div>
                ))}
              </AnimatePresence>
            </Stack>
            {hasMore && !loading && (
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
                <Button
                  variant="contained"
                  onClick={handleViewMore}
                  disabled={loadingMore}
                  sx={{
                    background: 'linear-gradient(90deg, #ff914d 0%, #e94e77 100%)',
                    color: '#fff',
                    fontWeight: 700,
                    fontSize: 18,
                    borderRadius: 2,
                    px: 5,
                    py: 1.5,
                    boxShadow: 'none',
                    '&:hover': {
                      background: 'linear-gradient(90deg, #ff914d 0%, #e94e77 100%)',
                      opacity: 0.92,
                    },
                  }}
                >
                  {loadingMore ? 'Loading...' : 'View More'}
                </Button>
              </Box>
            )}
          </>
        )}
      </Box>
    </Box>
  );
};