# Licensed under a 3-clause BSD style license - see LICENSE.rst

from astropy import units as u
from astropy.coordinates.baseframe import frame_transform_graph
from astropy.coordinates.transformations import FunctionTransformWithFiniteDifference
from astropy.coordinates.representation import (SphericalRepresentation,
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

@frame_transform_graph.transform(FunctionTransformWithFiniteDifference, ICRS, AltAz)
@frame_transform_graph.transform(FunctionTransformWithFiniteDifference, ICRS, HADec)
def icrs_to_observed(icrs_coo, observed_frame):
    is_unitspherical = (isinstance(icrs_coo.data, UnitSphericalRepresentation) or
                        icrs_coo.cartesian.x.unit == u.one)
    # first set up the astrometry context for ICRS<->observed
    astrom = erfa_astrom.get().apco(observed_frame)

    # correct for parallax to find BCRS direction from observer (as in erfa.pmpx)
    if is_unitspherical:
        srepr = icrs_coo.spherical
    # trying to keep this transform linear so that we're not just approximating for
    # the sake of a more computationally intensive transform.
    if isinstance(observed_frame, AltAz):
        # form ITRS to AltAz matrix
        elat = lat.to_value(u.radian)
        # AltAz frame is left handed
        minus_x = np.eye(3)
    # now perform observed conversion
    if isinstance(observed_frame, AltAz):
        lon, zen, _, _, _ = erfa.atioq(cirs_ra, cirs_dec, astrom)
        lat = PIOVER2 - zen
    else:
        _, _, lon, lat, _ = erfa.atioq(cirs_ra, cirs_dec, astrom)

    if is_unitspherical:
        minus_y = np.eye(3)
        minus_y[1][1] = -1.0
        mat = (minus_y
               @ rotation_matrix(elong, 'z', unit=u.radian))
    else:
        # form ITRS to HADec matrix
        # HADec frame is left handed
def observed_to_icrs(observed_coo, icrs_frame):
    # if the data are UnitSphericalRepresentation, we can skip the distance calculations
    is_unitspherical = (isinstance(observed_coo.data, UnitSphericalRepresentation) or
                        observed_coo.cartesian.x.unit == u.one)

    usrepr = observed_coo.represent_as(UnitSphericalRepresentation)
    lon = usrepr.lon.to_value(u.radian)
    lat = usrepr.lat.to_value(u.radian)
    return mat


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference, AltAz, ICRS)
@frame_transform_graph.transform(FunctionTransformWithFiniteDifference, HADec, ICRS)
def observed_to_icrs(observed_coo, icrs_frame):
                              
    # first set up the astrometry context for ICRS<->CIRS at the observed_coo time
    astrom = erfa_astrom.get().apco(observed_coo)

    # Topocentric CIRS
    cirs_ra, cirs_dec = erfa.atoiq(coord_type, lon, lat, astrom) << u.radian
    if is_unitspherical:
        srepr = SphericalRepresentation(cirs_ra, cirs_dec, 1, copy=False)
    else:
        srepr = SphericalRepresentation(lon=cirs_ra, lat=cirs_dec,
                                        distance=observed_coo.distance, copy=False)

    obs_srepr = observed_coo.represent_as(UnitSphericalRepresentation)
    lon = usrepr.lon.to_value(u.radian)
    lat = usrepr.lat.to_value(u.radian)
    # first set up the astrometry context for ICRS<->observed
    astrom = erfa_astrom.get().apco(observed_coo)
    if isinstance(observed_coo, AltAz):
        # the 'A' indicates zen/az inputs
        coord_type = 'A'
                                             distance=observed_coo.distance, copy=False)
        observer_icrs = CartesianRepresentation(astrom['eb'], unit=u.au, xyz_axis=-1, copy=False)
        newrepr = icrs_srepr.to_cartesian() + observer_icrs
        icrs_srepr = newrepr.represent_as(SphericalRepresentation)

    return icrs_frame.realize_frame(icrs_srepr)


# Create loopback transformations
frame_transform_graph._add_merged_transform(AltAz, ICRS, AltAz)
frame_transform_graph._add_merged_transform(HADec, ICRS, HADec)
    # Topocentric CIRS
    cirs_ra, cirs_dec = erfa.atoiq(coord_type, lon, lat, astrom) << u.radian
    if is_unitspherical:
        srepr = UnitSphericalRepresentation(cirs_ra, cirs_dec, copy=False)
    else:
        srepr = SphericalRepresentation(lon=cirs_ra, lat=cirs_dec,
                                       distance=observed_coo.distance, copy=False)
    if is_unitspherical:
        icrs_srepr = UnitSphericalRepresentation(bcrs_ra, bcrs_dec, copy=False)
    else:
        icrs_srepr = SphericalRepresentation(lon=bcrs_ra, lat=bcrs_dec,
                                            distance=observed_coo.distance, copy=False)
        observer_icrs = CartesianRepresentation(astrom['eb'], unit=u.au, xyz_axis=-1, copy=False)
        newrepr = icrs_srepr.to_cartesian() + observer_icrs
    # form the Topocentric ITRS position
    topocentric_itrs_repr = (observed_coo.cartesian
                             - observed_frame.location.get_itrs().cartesian)
    # first set up the astrometry context for ICRS<->observed
    astrom = erfa_astrom.get().apco(observed_frame)
    # form ITRS to AltAz matrix
    elat = lat.to_value(u.radian)
    # AltAz frame is left handed
    minus_x = np.eye(3)
    minus_x[0][0] = -1.0
    mat = (minus_x


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference, AltAz, ITRS)
@frame_transform_graph.transform(FunctionTransformWithFiniteDifference, HADec, ITRS)
def observed_to_icrs(observed_coo, itrs_frame):
    # Trying to synchronize the obstimes here makes no sense. In fact,
    # it's a real gotcha as doing an ITRS->ITRS transform references
    # ITRS coordinates, which should be tied to the Earth, to the SSB.
    # Instead, we treat ITRS coordinates as time invariant here.
    # form the Topocentric ITRS position
    topocentric_itrs_repr = (observed_coo.cartesian
                             - observed_frame.location.get_itrs().cartesian)
    # form the Geocentric ITRS position
    # form the Geocentric ITRS position
    rep = topocentric_itrs_repr.transform(itrs_to_observed_mat(observed_frame))
    return observed_frame.realize_frame(rep)

@frame_transform_graph.transform(FunctionTransformWithFiniteDifference, AltAz, ITRS)
@frame_transform_graph.transform(FunctionTransformWithFiniteDifference, HADec, ITRS)
def observed_to_icrs(observed_coo, itrs_frame):


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference, AltAz, ITRS)
@frame_transform_graph.transform(FunctionTransformWithFiniteDifference, HADec, ITRS)
def observed_to_icrs(observed_coo, itrs_frame):
    # Trying to synchronize the obstimes here makes no sense. In fact,
    # it's a real gotcha as doing an ITRS->ITRS transform references
    # ITRS coordinates, which should be tied to the Earth, to the SSB.
    # Instead, we treat ITRS coordinates as time invariant here.
    return observed_frame.realize_frame(rep)


