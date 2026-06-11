# Licensed under a 3-clause BSD style license - see LICENSE.rst

from astropy import units as u
from astropy.coordinates.baseframe import frame_transform_graph
from astropy.coordinates.transformations import FunctionTransformWithFiniteDifference
from astropy import units as u
from astropy.coordinates.builtin_frames.utils import atciqz, aticq
from astropy.coordinates.baseframe import frame_transform_graph
from astropy.coordinates.transformations import FunctionTransformWithFiniteDifference
from astropy.coordinates.representation import (SphericalRepresentation,
                                                CartesianRepresentation,
                                                UnitSphericalRepresentation)

from .icrs import ICRS
from .altaz import AltAz
from .hadec import HADec
from .utils import PIOVER2
from ..erfa_astrom import erfa_astrom

def itrs_to_observed_mat(observed_frame):
    """
    Form the transformation matrix from ITRS to observed frame (AltAz or HADec).
    is_unitspherical = (isinstance(icrs_coo.data, UnitSphericalRepresentation) or
                        icrs_coo.cartesian.x.unit == u.one)
    lon, lat, height = observed_frame.location.to_geodetic('WGS84')
    elong = lon.to_value(u.radian)

    if isinstance(observed_frame, AltAz):
        # form ITRS to AltAz matrix
        elat = lat.to_value(u.radian)
        # AltAz frame is left handed
        minus_x = np.eye(3)
        minus_x[0][0] = -1.0
        mat = (minus_x
               @ rotation_matrix(PIOVER2 - elat, 'y', unit=u.radian)
               @ rotation_matrix(elong, 'z', unit=u.radian))
    else:
        # form ITRS to HADec matrix
        # HADec frame is left handed
        minus_y = np.eye(3)
        minus_y[1][1] = -1.0
        mat = (minus_y
               @ rotation_matrix(elong, 'z', unit=u.radian))

    return mat


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference, ITRS, AltAz)
@frame_transform_graph.transform(FunctionTransformWithFiniteDifference, ITRS, HADec)
def itrs_to_observed(itrs_coo, observed_frame):
    """
    Transform from ITRS to observed frame (AltAz or HADec).

    This transformation stays within ITRS and does not adjust obstime.
    ITRS coordinates are treated as time-invariant for objects on Earth.
    """
    # Trying to synchronize the obstimes here makes no sense. In fact,
    # it's a real gotcha as doing an ITRS->ITRS transform references 
    # ITRS coordinates, which should be tied to the Earth, to the SSB.
    # Instead, we treat ITRS coordinates as time invariant here.

    # form the Topocentric ITRS position
    topocentric_itrs_repr = (itrs_coo.cartesian
                             - observed_frame.location.get_itrs().cartesian)
    rep = topocentric_itrs_repr.transform(itrs_to_observed_mat(observed_frame))
    return observed_frame.realize_frame(rep)


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference, AltAz, ITRS)
@frame_transform_graph.transform(FunctionTransformWithFiniteDifference, HADec, ITRS)
def observed_to_itrs(observed_coo, itrs_frame):
    """
    Transform from observed frame (AltAz or HADec) to ITRS.

    This transformation stays within ITRS and does not adjust obstime.
    ITRS coordinates are treated as time-invariant for objects on Earth.
    """
    # Trying to synchronize the obstimes here makes no sense. In fact,
    # it's a real gotcha as doing an ITRS->ITRS transform references 
    # ITRS coordinates, which should be tied to the Earth, to the SSB.
    # Instead, we treat ITRS coordinates as time invariant here.

    # form the Topocentric ITRS position
    topocentric_itrs_repr = observed_coo.cartesian.transform(matrix_transpose(
                            itrs_to_observed_mat(observed_coo)))
    # form the Geocentric ITRS position
    rep = topocentric_itrs_repr + observed_coo.location.get_itrs().cartesian
    return itrs_frame.realize_frame(rep)
    else:
        srepr = SphericalRepresentation(lon=cirs_ra, lat=cirs_dec,
                                        distance=observed_coo.distance, copy=False)

    # BCRS (Astrometric) direction to source
    bcrs_ra, bcrs_dec = aticq(srepr, astrom) << u.radian

    # Correct for parallax to get ICRS representation
    if is_unitspherical:
        icrs_srepr = UnitSphericalRepresentation(bcrs_ra, bcrs_dec, copy=False)
    else:
        icrs_srepr = SphericalRepresentation(lon=bcrs_ra, lat=bcrs_dec,
                                             distance=observed_coo.distance, copy=False)
        observer_icrs = CartesianRepresentation(astrom['eb'], unit=u.au, xyz_axis=-1, copy=False)
        newrepr = icrs_srepr.to_cartesian() + observer_icrs
        icrs_srepr = newrepr.represent_as(SphericalRepresentation)

    return icrs_frame.realize_frame(icrs_srepr)


# Create loopback transformations
frame_transform_graph._add_merged_transform(AltAz, ICRS, AltAz)
frame_transform_graph._add_merged_transform(HADec, ICRS, HADec)
# for now we just implement this through ICRS to make sure we get everything
# covered
# Before, this was using CIRS as intermediate frame, however this is much
# slower than the direct observed<->ICRS transform added in 4.3
# due to how the frame attribute broadcasting works, see
# https://github.com/astropy/astropy/pull/10994#issuecomment-722617041
