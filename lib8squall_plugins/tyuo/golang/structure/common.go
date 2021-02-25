package structure
import (
    "github.com/juju/loggo"
    "math/rand"
    "time"
)

var logger = loggo.GetLogger("core_stats")

const rescaleThreshold int = 1000
const rescaleDecimator int = 3

const sentenceBoundary int = -2147483648 //used to denote the end of a sentence

var rng := rand.Rand.New(rand.NewSource(time.Now().Unix()))
