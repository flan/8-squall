package structure
import (
    "github.com/juju/loggo"
    "math/rand"
    "time"
)

var logger = loggo.GetLogger("core_stats")

const rescaleThreshold int = 100
const rescaleDecimator int = 4

var rng := rand.Rand.New(rand.NewSource(time.Now().Unix()))
